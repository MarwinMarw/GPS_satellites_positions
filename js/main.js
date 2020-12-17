import { GLTFLoader } from '../node_modules/three/examples/jsm/loaders/GLTFLoader.js';
import { OBJLoader } from '../node_modules/three/examples/jsm/loaders/OBJLoader.js';
import { OrbitControls } from '../node_modules/three/examples/jsm/controls/OrbitControls.js';

let text = document.getElementById('info');

let renderer, scene, camera;
let PLANET = null;
let t = 0;

scene = new THREE.Scene();
scene.background = new THREE.Color(0x5199FF)

camera = new THREE.PerspectiveCamera(50, window.innerWidth/window.innerHeight, 0.1, 2000);
camera.position.set(0, 0, 25);

renderer = new THREE.WebGLRenderer();
renderer.setSize(window.innerWidth, window.innerHeight);
document.body.appendChild(renderer.domElement);

initLights();
const control = new OrbitControls(camera, renderer.domElement);
control.update();
const gltfLoader = new GLTFLoader();
const objLoader = new OBJLoader();


class Satellite{	
	constructor(dirScene){
		gltfLoader.load('./3d_models/Satellite.glb', (object) => {
			//object.scene.scale.set(0.4, 0.4, 0.4);
			this.SATELLITE = object;	
			this.SATELLITE.scene.rotateZ(1.5);
			this.SATELLITE.scene.position.set(10, 0, 0);
			dirScene.add(this.SATELLITE.scene);
		});
	}


	
}


let sat = new Satellite(scene);

gltfLoader.load('./3d_models/Earth/scene.gltf', (object) => {
	object.scene.scale.set(0.001, 0.001, 0.001);
	PLANET = object;	
	
	scene.add(PLANET.scene);
});



window.addEventListener('resize', function(){
	renderer.setSize(window.innerWidth, window.innerHeight);

})



animate();

function animate(){
	t += 0.01;
	animateSatellite();
	animatePlanet();
	text.innerHTML = camera.position.x + " " + camera.position.y + " " + camera.position.z
	requestAnimationFrame(animate);
	renderer.render(scene, camera);
}



function initLights() {
    const ambient = new THREE.AmbientLight(0xffffff, 0.7);
    scene.add(ambient);

    const directionalLight = new THREE.DirectionalLight(0xffffff);
    directionalLight.position.set(0, 1, 1);
    scene.add(directionalLight);
}

function animatePlanet(){
	if(PLANET != null){
		PLANET.scene.rotateY(0.003);
	}
}

function animateSatellite(){
	if(sat.SATELLITE != null && PLANET != null){
		let x = PLANET.scene.position.x + 8 * Math.cos(t);
		let z = PLANET.scene.position.z + 8 * Math.sin(t);
		let y = PLANET.scene.position.y;

		sat.SATELLITE.scene.position.set(x, y, z);
		sat.SATELLITE.scene.rotateX(-0.01);
	}	
}

