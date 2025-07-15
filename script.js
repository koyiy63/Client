class CubeSimulator {
    constructor() {
        this.scene = null;
        this.camera = null;
        this.renderer = null;
        this.cube = null;
        this.lights = [];
        
        // Control variables
        this.isMouseDown = false;
        this.mouseX = 0;
        this.mouseY = 0;
        this.rotationX = 0;
        this.rotationY = 0;
        this.targetRotationX = 0;
        this.targetRotationY = 0;
        this.autoRotationSpeed = 0;
        
        // Touch control variables
        this.touchStartX = 0;
        this.touchStartY = 0;
        this.touchStartRotationX = 0;
        this.touchStartRotationY = 0;
        this.isTouching = false;
        
        // Performance tracking
        this.frameCount = 0;
        this.lastTime = 0;
        this.fps = 60;
        
        // Materials
        this.materials = {};
        this.currentMaterial = 'basic';
        
        this.init();
    }
    
    init() {
        this.setupScene();
        this.setupCamera();
        this.setupRenderer();
        this.setupLights();
        this.createCube();
        this.setupMaterials();
        this.setupControls();
        this.setupEventListeners();
        this.animate();
    }
    
    setupScene() {
        this.scene = new THREE.Scene();
        this.scene.background = new THREE.Color(0x1a1a2e);
    }
    
    setupCamera() {
        const canvas = document.getElementById('cube-canvas');
        const aspect = canvas.clientWidth / canvas.clientHeight;
        
        this.camera = new THREE.PerspectiveCamera(75, aspect, 0.1, 1000);
        this.camera.position.set(0, 0, 5);
    }
    
    setupRenderer() {
        const canvas = document.getElementById('cube-canvas');
        
        this.renderer = new THREE.WebGLRenderer({
            canvas: canvas,
            antialias: true,
            alpha: true,
            powerPreference: "high-performance"
        });
        
        this.renderer.setSize(canvas.clientWidth, canvas.clientHeight);
        this.renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
        this.renderer.shadowMap.enabled = true;
        this.renderer.shadowMap.type = THREE.PCFSoftShadowMap;
        this.renderer.outputEncoding = THREE.sRGBEncoding;
    }
    
    setupLights() {
        // Ambient light
        const ambientLight = new THREE.AmbientLight(0x404040, 0.4);
        this.scene.add(ambientLight);
        this.lights.push(ambientLight);
        
        // Directional light
        const directionalLight = new THREE.DirectionalLight(0xffffff, 0.8);
        directionalLight.position.set(5, 5, 5);
        directionalLight.castShadow = true;
        directionalLight.shadow.mapSize.width = 2048;
        directionalLight.shadow.mapSize.height = 2048;
        this.scene.add(directionalLight);
        this.lights.push(directionalLight);
        
        // Point light for dynamic lighting
        const pointLight = new THREE.PointLight(0x667eea, 0.5, 10);
        pointLight.position.set(-3, 2, 3);
        this.scene.add(pointLight);
        this.lights.push(pointLight);
    }
    
    createCube() {
        const geometry = new THREE.BoxGeometry(2, 2, 2);
        const material = new THREE.MeshPhongMaterial({
            color: 0x667eea,
            shininess: 100,
            transparent: true,
            opacity: 0.9
        });
        
        this.cube = new THREE.Mesh(geometry, material);
        this.cube.castShadow = true;
        this.cube.receiveShadow = true;
        this.scene.add(this.cube);
        
        // Update vertex count display
        document.getElementById('vertex-count').textContent = geometry.attributes.position.count;
    }
    
    setupMaterials() {
        // Basic material
        this.materials.basic = new THREE.MeshPhongMaterial({
            color: 0x667eea,
            shininess: 100,
            transparent: true,
            opacity: 0.9
        });
        
        // Metal material
        this.materials.metal = new THREE.MeshPhongMaterial({
            color: 0x888888,
            shininess: 200,
            metalness: 0.8,
            roughness: 0.2
        });
        
        // Glass material
        this.materials.glass = new THREE.MeshPhongMaterial({
            color: 0xffffff,
            shininess: 300,
            transparent: true,
            opacity: 0.3,
            refractionRatio: 0.98
        });
        
        // Wood material
        this.materials.wood = new THREE.MeshPhongMaterial({
            color: 0x8B4513,
            shininess: 30,
            roughness: 0.8
        });
        
        // Neon material
        this.materials.neon = new THREE.MeshPhongMaterial({
            color: 0x00ff88,
            shininess: 100,
            emissive: 0x00ff88,
            emissiveIntensity: 0.3,
            transparent: true,
            opacity: 0.8
        });
    }
    
    setupControls() {
        // Material selector
        const materialSelect = document.getElementById('material-select');
        materialSelect.addEventListener('change', (e) => {
            this.currentMaterial = e.target.value;
            this.cube.material = this.materials[this.currentMaterial];
        });
        
        // Rotation speed slider
        const rotationSpeedSlider = document.getElementById('rotation-speed');
        const speedValue = document.getElementById('speed-value');
        
        rotationSpeedSlider.addEventListener('input', (e) => {
            this.autoRotationSpeed = parseFloat(e.target.value);
            speedValue.textContent = this.autoRotationSpeed.toFixed(1);
        });
        
        // Reset button
        const resetBtn = document.getElementById('reset-btn');
        resetBtn.addEventListener('click', () => {
            this.resetView();
        });
        
        // Fullscreen button
        const fullscreenBtn = document.getElementById('fullscreen-btn');
        fullscreenBtn.addEventListener('click', () => {
            this.toggleFullscreen();
        });
    }
    
    setupEventListeners() {
        const canvas = document.getElementById('cube-canvas');
        
        // Mouse events
        canvas.addEventListener('mousedown', (e) => this.onMouseDown(e));
        canvas.addEventListener('mousemove', (e) => this.onMouseMove(e));
        canvas.addEventListener('mouseup', () => this.onMouseUp());
        canvas.addEventListener('wheel', (e) => this.onWheel(e));
        
        // Touch events for mobile
        canvas.addEventListener('touchstart', (e) => this.onTouchStart(e), { passive: false });
        canvas.addEventListener('touchmove', (e) => this.onTouchMove(e), { passive: false });
        canvas.addEventListener('touchend', () => this.onTouchEnd());
        
        // Window resize
        window.addEventListener('resize', () => this.onWindowResize());
        
        // Prevent context menu on right click
        canvas.addEventListener('contextmenu', (e) => e.preventDefault());
    }
    
    onMouseDown(e) {
        this.isMouseDown = true;
        this.mouseX = e.clientX;
        this.mouseY = e.clientY;
    }
    
    onMouseMove(e) {
        if (!this.isMouseDown) return;
        
        const deltaX = e.clientX - this.mouseX;
        const deltaY = e.clientY - this.mouseY;
        
        this.targetRotationY += deltaX * 0.01;
        this.targetRotationX += deltaY * 0.01;
        
        this.mouseX = e.clientX;
        this.mouseY = e.clientY;
    }
    
    onMouseUp() {
        this.isMouseDown = false;
    }
    
    onWheel(e) {
        e.preventDefault();
        const zoomSpeed = 0.1;
        const delta = e.deltaY > 0 ? 1 : -1;
        
        this.camera.position.z += delta * zoomSpeed;
        this.camera.position.z = Math.max(2, Math.min(10, this.camera.position.z));
    }
    
    onTouchStart(e) {
        e.preventDefault();
        this.isTouching = true;
        
        if (e.touches.length === 1) {
            this.touchStartX = e.touches[0].clientX;
            this.touchStartY = e.touches[0].clientY;
            this.touchStartRotationX = this.targetRotationX;
            this.touchStartRotationY = this.targetRotationY;
        }
    }
    
    onTouchMove(e) {
        e.preventDefault();
        
        if (e.touches.length === 1 && this.isTouching) {
            const touch = e.touches[0];
            const deltaX = touch.clientX - this.touchStartX;
            const deltaY = touch.clientY - this.touchStartY;
            
            this.targetRotationY = this.touchStartRotationY + deltaX * 0.01;
            this.targetRotationX = this.touchStartRotationX + deltaY * 0.01;
        } else if (e.touches.length === 2) {
            // Pinch to zoom
            const touch1 = e.touches[0];
            const touch2 = e.touches[1];
            
            const currentDistance = Math.hypot(
                touch1.clientX - touch2.clientX,
                touch1.clientY - touch2.clientY
            );
            
            if (this.lastTouchDistance) {
                const delta = (currentDistance - this.lastTouchDistance) * 0.01;
                this.camera.position.z -= delta;
                this.camera.position.z = Math.max(2, Math.min(10, this.camera.position.z));
            }
            
            this.lastTouchDistance = currentDistance;
        }
    }
    
    onTouchEnd() {
        this.isTouching = false;
        this.lastTouchDistance = null;
    }
    
    onWindowResize() {
        const canvas = document.getElementById('cube-canvas');
        const width = canvas.clientWidth;
        const height = canvas.clientHeight;
        
        this.camera.aspect = width / height;
        this.camera.updateProjectionMatrix();
        
        this.renderer.setSize(width, height);
    }
    
    resetView() {
        this.targetRotationX = 0;
        this.targetRotationY = 0;
        this.camera.position.set(0, 0, 5);
        this.autoRotationSpeed = 0;
        document.getElementById('rotation-speed').value = 0;
        document.getElementById('speed-value').textContent = '0';
    }
    
    toggleFullscreen() {
        const container = document.querySelector('.container');
        
        if (!document.fullscreenElement) {
            container.requestFullscreen().catch(err => {
                console.log('Error attempting to enable fullscreen:', err);
            });
            container.classList.add('fullscreen');
        } else {
            document.exitFullscreen();
            container.classList.remove('fullscreen');
        }
    }
    
    updateFPS() {
        this.frameCount++;
        const currentTime = performance.now();
        
        if (currentTime - this.lastTime >= 1000) {
            this.fps = Math.round((this.frameCount * 1000) / (currentTime - this.lastTime));
            document.getElementById('fps-counter').textContent = this.fps;
            this.frameCount = 0;
            this.lastTime = currentTime;
        }
    }
    
    animate() {
        requestAnimationFrame(() => this.animate());
        
        // Smooth rotation interpolation
        this.rotationX += (this.targetRotationX - this.rotationX) * 0.1;
        this.rotationY += (this.targetRotationY - this.rotationY) * 0.1;
        
        // Auto rotation
        if (this.autoRotationSpeed > 0) {
            this.targetRotationY += this.autoRotationSpeed * 0.02;
        }
        
        // Apply rotations
        this.cube.rotation.x = this.rotationX;
        this.cube.rotation.y = this.rotationY;
        
        // Animate lights for dynamic effect
        this.lights[2].position.x = Math.sin(Date.now() * 0.001) * 3;
        this.lights[2].position.z = Math.cos(Date.now() * 0.001) * 3;
        
        // Render
        this.renderer.render(this.scene, this.camera);
        
        // Update FPS counter
        this.updateFPS();
    }
}

// Initialize the simulator when the page loads
document.addEventListener('DOMContentLoaded', () => {
    // Check for WebGL support
    if (!window.WebGLRenderingContext) {
        alert('WebGL is not supported in your browser. Please use a modern browser.');
        return;
    }
    
    try {
        new CubeSimulator();
    } catch (error) {
        console.error('Error initializing Cube Simulator:', error);
        alert('Failed to initialize the 3D cube simulator. Please refresh the page.');
    }
});

// Service Worker for PWA capabilities (optional)
if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        navigator.serviceWorker.register('/sw.js')
            .then(registration => {
                console.log('SW registered: ', registration);
            })
            .catch(registrationError => {
                console.log('SW registration failed: ', registrationError);
            });
    });
}