import { GLTFLoader } from './GLTFLoader.js'

const scene = new THREE.Scene()
const sizes = {
	width: window.innerWidth,
	height: window.innerHeight,
}

const camera = new THREE.PerspectiveCamera(75, sizes.width / sizes.height, 0.01, 1000)

const renderer = new THREE.WebGLRenderer()
renderer.setSize(sizes.width, sizes.height)
document.body.appendChild(renderer.domElement)

const loader = new GLTFLoader()
var obj

loader.load('scene.gltf', function (gltf) {
	obj = gltf.scene
	obj.position.set(0, 0, -3)
	scene.add(gltf.scene)
})

const light = new THREE.PointLight(0xfee6d8, 1, 100)
light.position.set(0, 4, 3)
light.intensity = 1
scene.add(light)
camera.position.set(0, 0, 0.5)

function animate(time) {
	requestAnimationFrame(animate)
	renderer.render(scene, camera)
}
animate()
