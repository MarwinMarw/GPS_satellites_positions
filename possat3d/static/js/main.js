import { GLTFLoader } from '../node_modules/three/examples/jsm/loaders/GLTFLoader.js';
import { OBJLoader } from '../node_modules/three/examples/jsm/loaders/OBJLoader.js';
import { OrbitControls } from '../node_modules/three/examples/jsm/controls/OrbitControls.js';

add_sat = addSatellite

var info_el = document.getElementById('info')

var satellites = []

let renderer, scene, camera;
let PLANET = null;
let t = 0;

scene = new THREE.Scene();
scene.background = new THREE.Color(0x5199FF)
ajaxRINEXget()


camera = new THREE.PerspectiveCamera(50, window.innerWidth/window.innerHeight, 0.1, 2000);
camera.position.set(0, 0, 45);

renderer = new THREE.WebGLRenderer();
renderer.setSize(window.innerWidth, window.innerHeight);
document.body.appendChild(renderer.domElement);

initLights();
const control = new OrbitControls(camera, renderer.domElement);
control.update();
const gltfLoader = new GLTFLoader();
const objLoader = new OBJLoader();


class Satellite{	
	constructor(dirScene, name, position){

		this.name = name;
		gltfLoader.load('static/3d_models/satLite.glb', (object) => {
			this.scaleConst = 1000000
			this.SATELLITE = object;	
			this.SATELLITE.scene.rotateZ(1.5);
			this.SATELLITE.scene.position.set(
				position[0]/this.scaleConst,
				position[1]/this.scaleConst,
				position[2]/this.scaleConst
				  );

			console.log(this.name + " added to scene")
			dirScene.add(this.SATELLITE.scene);
		});
	}	
}


gltfLoader.load('static/3d_models/earthLite.glb', (object) => {
	object.scene.scale.set(2.0, 2.0, 2.0);
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
	requestAnimationFrame(animate);
	renderer.render(scene, camera);
}

//addSatellite('21', [20.0, 20.0, 20.0])

function addSatellite(name, pos){
	satellites.push(new Satellite(scene, name, pos))
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
	satellites.forEach(satellite => {
		if(satellite.SATELLITE != null && PLANET != null){
			satellite.SATELLITE.scene.rotateX(-0.01);
		}	
	})
}

