// macOS native offline render of the committed STL / folded-site scene manifest.
import Foundation
import SceneKit
import AppKit

let input = URL(fileURLWithPath: CommandLine.arguments[1])
let doc = try JSONSerialization.jsonObject(with: Data(contentsOf: input)) as! [String: Any]
let parts = doc["parts"] as! [[String: Any]]
let finishes = doc["materials"] as! [String: [Any]]
let params = doc["params"] as! [String: Any]
let out = doc["out"] as! String
let scene = SCNScene()
scene.background.contents = NSColor(srgbRed: 0.76, green: 0.74, blue: 0.71, alpha: 1)
scene.lightingEnvironment.contents = NSColor(srgbRed: 0.68, green: 0.68, blue: 0.68, alpha: 1)
scene.lightingEnvironment.intensity = 0.9

func number(_ key: String) -> Double { (params[key] as! NSNumber).doubleValue }
func vector(_ x: Double, _ y: Double, _ z: Double) -> SCNVector3 { SCNVector3(x,y,z) }
func plus(_ a:SCNVector3,_ b:SCNVector3)->SCNVector3 { vector(Double(a.x+b.x), Double(a.y+b.y), Double(a.z+b.z)) }
func point(_ u: Double, _ s: Double, _ y: Double) -> SCNVector3 {
    let r = number("PATH_RADIUS"), a = asin(number("TOTAL_CHORD")/(2*r))-s/r
    return vector(number("CREASE_BOW")-r+(r+u)*cos(a), y, -number("TOTAL_CHORD")/2+(r+u)*sin(a))
}
let target = point(number("BODY_WIDTH")/2, number("BODY_ARC")/2, 4)

func mesh(_ url: URL, _ name: String, _ finish: String) throws -> SCNNode {
    let data = try Data(contentsOf: url)
    let count = data.withUnsafeBytes { $0.loadUnaligned(fromByteOffset:80, as:UInt32.self) }.littleEndian
    guard data.count == 84 + Int(count)*50 else { throw NSError(domain:"STL",code:1) }
    var positions = [SCNVector3](); positions.reserveCapacity(Int(count)*3)
    var normals = [SCNVector3](); normals.reserveCapacity(Int(count)*3)
    data.withUnsafeBytes { raw in
        func f(_ at:Int)->Float { Float(bitPattern:raw.loadUnaligned(fromByteOffset:at,as:UInt32.self).littleEndian) }
        for i in 0..<Int(count) {
            let base=84+i*50
            let normal=vector(Double(f(base)),Double(f(base+4)),Double(f(base+8)))
            for j in 0..<3 {
                let off=base+12+j*12
                positions.append(vector(Double(f(off)),Double(f(off+4)),Double(f(off+8))))
                normals.append(normal)
            }
        }
    }
    let indices = Array(UInt32(0)..<UInt32(positions.count))
    let element = indices.withUnsafeBufferPointer { ptr in
        SCNGeometryElement(data: Data(buffer:ptr), primitiveType:.triangles,
                           primitiveCount:Int(count), bytesPerIndex:MemoryLayout<UInt32>.size)
    }
    let geometry=SCNGeometry(sources:[SCNGeometrySource(vertices:positions),SCNGeometrySource(normals:normals)],elements:[element])
    let spec=finishes[finish]!
    let rgba=spec[0] as! [Double]
    let material=SCNMaterial()
    material.name=finish
    material.lightingModel = .blinn
    material.diffuse.contents=NSColor(srgbRed:rgba[0],green:rgba[1],blue:rgba[2],alpha:1)
    material.specular.contents=NSColor(white:finish == "titanium" ? 0.68 : 0.25,alpha:1)
    material.shininess = finish == "titanium" ? 0.7 : 0.1
    material.isDoubleSided=true
    geometry.materials=[material]
    let node=SCNNode(geometry:geometry);node.name=name
    return node
}
var grouped=[String:[SCNNode]]()
for part in parts {
    let node=try mesh(URL(fileURLWithPath:part["path"] as! String),part["name"] as! String,part["material"] as! String)
    scene.rootNode.addChildNode(node)
    grouped[part["group"] as! String, default:[]].append(node)
}
func lamp(_ name:String, _ pos:SCNVector3, _ intensity:CGFloat) {
    let light=SCNLight();light.type = .omni;light.intensity=intensity
    light.color=NSColor.white
    let node=SCNNode();node.name=name;node.light=light;node.position=pos
    scene.rootNode.addChildNode(node)
}
let ambient=SCNLight();ambient.type = .ambient;ambient.color=NSColor(white:0.62,alpha:1)
let ambientNode=SCNNode();ambientNode.light=ambient;scene.rootNode.addChildNode(ambientNode)
lamp("key",plus(target,vector(-35,-30,35)),1700)
lamp("fill",plus(target,vector(40,23,7)),1300)
lamp("rim",plus(target,vector(10,28,-35)),1600)
let camera=SCNCamera();camera.usesOrthographicProjection=true;camera.zNear=0.1;camera.zFar=400
camera.wantsHDR=false
let cameraNode=SCNNode();cameraNode.camera=camera;scene.rootNode.addChildNode(cameraNode)
let renderer=SCNRenderer(device:nil,options:nil)
renderer.scene=scene
renderer.pointOfView=cameraNode
let views:[(String,SCNVector3,Double)] = [
    ("lateral",vector(35,82,55),84),("medial",vector(-27,-89,55),84),
    ("top",vector(28,28,95),82),("three_quarter",vector(78,80,71),96),
    ("exploded",vector(65,90,64),100),("inside_lid_off",vector(-35,85,75),110),
    ("quarter_scale",vector(78,80,71),88),("old_new",vector(35,82,55),135)]
for (view, offset, scale) in views {
    for node in grouped["lid"] ?? [] {
        node.position=vector(view == "exploded" ? number("BODY_WIDTH")*1.25 : view == "inside_lid_off" ? number("BODY_WIDTH")*2 : 0,
                             view == "exploded" ? 9 : 0,0)
    }
    for node in grouped["old"] ?? [] {
        node.isHidden = view != "old_new"
        node.position=vector(-27,0,0)
    }
    for node in grouped["coin"] ?? [] { node.isHidden = view != "quarter_scale" }
    camera.orthographicScale=scale
    let aim = plus(target,vector(view == "old_new" ? -12 : 0,0,0))
    cameraNode.position=plus(aim,offset)
    cameraNode.look(at:aim,up:vector(0,1,0),localFront:vector(0,0,-1))
    let image=renderer.snapshot(atTime:0,with:CGSize(width:1050,height:1300),antialiasingMode:.multisampling4X)
    guard let tiff=image.tiffRepresentation, let bitmap=NSBitmapImageRep(data:tiff),
          let png=bitmap.representation(using:.png,properties:[:]) else { fatalError("snapshot failed") }
    try png.write(to:URL(fileURLWithPath:out+"/"+view+".png"))
    print("rendered \(view)")
}
