class CubeSimulator {
    constructor() {
        this.scene = null;
        this.camera = null;
        this.renderer = null;
        this.controls = null;
        this.cube = null;
        this.cubeGroup = null;
        this.isMobile = this.detectMobile();
        this.autoRotate = true;
        this.rotationSpeed = 1;
        this.cubeSize = 1;
        this.wireframe = false;
        this.initialCameraPosition = { x: 5, y: 5, z: 5 };
        
        this.init();
        this.setupEventListeners();
        this.animate();
    }
    
    detectMobile() {
        return /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent) ||
               window.innerWidth <= 768;
    }
    
    init() {
        // Create scene
        this.scene = new THREE.Scene();
        this.scene.background = new THREE.Color(0x000000);
        
        // Create camera
        const aspect = window.innerWidth / window.innerHeight;
        this.camera = new THREE.PerspectiveCamera(75, aspect, 0.1, 1000);
        this.camera.position.set(this.initialCameraPosition.x, this.initialCameraPosition.y, this.initialCameraPosition.z);
        
        // Create renderer
        this.renderer = new THREE.WebGLRenderer({ 
            canvas: document.getElementById('cube-canvas'),
            antialias: true,
            alpha: true,
            powerPreference: "high-performance"
        });
        this.renderer.setSize(window.innerWidth, window.innerHeight);
        this.renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2)); // Limit pixel ratio for performance
        this.renderer.shadowMap.enabled = true;
        this.renderer.shadowMap.type = THREE.PCFSoftShadowMap;
        
        // Create controls
        this.controls = new THREE.OrbitControls(this.camera, this.renderer.domElement);
        this.controls.enableDamping = true;
        this.controls.dampingFactor = 0.05;
        this.controls.enableZoom = true;
        this.controls.enablePan = true;
        this.controls.autoRotate = this.autoRotate;
        this.controls.autoRotateSpeed = 2.0;
        
        // Mobile-specific controls
        if (this.isMobile) {
            this.controls.enableKeys = false;
            this.controls.touches = {
                ONE: THREE.TOUCH.ROTATE,
                TWO: THREE.TOUCH.DOLLY_PAN
            };
        }
        
        // Add lighting
        this.setupLighting();
        
        // Create cube
        this.createCube();
        
        // Handle window resize
        window.addEventListener('resize', () => this.onWindowResize());
    }
    
    setupLighting() {
        // Ambient light
        const ambientLight = new THREE.AmbientLight(0x404040, 0.4);
        this.scene.add(ambientLight);
        
        // Directional light
        const directionalLight = new THREE.DirectionalLight(0xffffff, 0.8);
        directionalLight.position.set(10, 10, 5);
        directionalLight.castShadow = true;
        directionalLight.shadow.mapSize.width = 2048;
        directionalLight.shadow.mapSize.height = 2048;
        this.scene.add(directionalLight);
        
        // Point light for better mobile performance
        const pointLight = new THREE.PointLight(0xffffff, 0.5);
        pointLight.position.set(-10, -10, -5);
        this.scene.add(pointLight);
    }
    
    createCube() {
        this.cubeGroup = new THREE.Group();
        
        // Create a 3x3x3 Rubik's cube structure
        const cubeSize = 0.5;
        const gap = 0.05;
        const totalSize = cubeSize + gap;
        
        const colors = [
            0xff0000, // Red
            0x00ff00, // Green
            0x0000ff, // Blue
            0xffff00, // Yellow
            0xff8800, // Orange
            0xffffff  // White
        ];
        
        const geometry = new THREE.BoxGeometry(cubeSize, cubeSize, cubeSize);
        
        for (let x = -1; x <= 1; x++) {
            for (let y = -1; y <= 1; y++) {
                for (let z = -1; z <= 1; z++) {
                    // Skip center cube
                    if (x === 0 && y === 0 && z === 0) continue;
                    
                    const material = new THREE.MeshPhongMaterial({
                        color: colors[Math.floor(Math.random() * colors.length)],
                        shininess: 100,
                        transparent: true,
                        opacity: 0.9
                    });
                    
                    const cube = new THREE.Mesh(geometry, material);
                    cube.position.set(x * totalSize, y * totalSize, z * totalSize);
                    cube.castShadow = true;
                    cube.receiveShadow = true;
                    
                    this.cubeGroup.add(cube);
                }
            }
        }
        
        this.scene.add(this.cubeGroup);
    }
    
    setupEventListeners() {
        // Desktop controls
        document.getElementById('reset-cube').addEventListener('click', () => this.resetCube());
        document.getElementById('random-rotate').addEventListener('click', () => this.randomRotate());
        document.getElementById('solve-cube').addEventListener('click', () => this.solveCube());
        document.getElementById('reset-camera').addEventListener('click', () => this.resetCamera());
        document.getElementById('top-view').addEventListener('click', () => this.setTopView());
        document.getElementById('front-view').addEventListener('click', () => this.setFrontView());
        
        // Sliders and toggles
        document.getElementById('cube-size').addEventListener('input', (e) => {
            this.cubeSize = parseFloat(e.target.value);
            this.updateCubeSize();
        });
        
        document.getElementById('rotation-speed').addEventListener('input', (e) => {
            this.rotationSpeed = parseFloat(e.target.value);
            this.controls.autoRotateSpeed = this.rotationSpeed * 2;
        });
        
        document.getElementById('wireframe-toggle').addEventListener('change', (e) => {
            this.wireframe = e.target.checked;
            this.updateWireframe();
        });
        
        // Mobile controls
        document.getElementById('mobile-reset').addEventListener('click', () => this.resetCube());
        document.getElementById('mobile-random').addEventListener('click', () => this.randomRotate());
        document.getElementById('mobile-solve').addEventListener('click', () => this.solveCube());
        
        // Touch events for mobile
        if (this.isMobile) {
            this.setupMobileTouchEvents();
        }
        
        // Keyboard controls
        document.addEventListener('keydown', (e) => this.handleKeyPress(e));
    }
    
    setupMobileTouchEvents() {
        let touchStartTime = 0;
        let touchCount = 0;
        
        this.renderer.domElement.addEventListener('touchstart', (e) => {
            touchStartTime = Date.now();
            touchCount = e.touches.length;
        });
        
        this.renderer.domElement.addEventListener('touchend', (e) => {
            const touchDuration = Date.now() - touchStartTime;
            
            // Double tap detection
            if (touchDuration < 300 && touchCount === 1) {
                this.resetCube();
            }
        });
        
        // Show/hide controls panel on mobile
        let lastTouchY = 0;
        this.renderer.domElement.addEventListener('touchmove', (e) => {
            const touchY = e.touches[0].clientY;
            const deltaY = touchY - lastTouchY;
            
            if (Math.abs(deltaY) > 50) {
                const controlsPanel = document.getElementById('controls-panel');
                if (deltaY > 0) {
                    controlsPanel.classList.add('show');
                } else {
                    controlsPanel.classList.remove('show');
                }
            }
            
            lastTouchY = touchY;
        });
    }
    
    handleKeyPress(e) {
        switch(e.key) {
            case 'r':
            case 'R':
                this.resetCube();
                break;
            case ' ':
                e.preventDefault();
                this.randomRotate();
                break;
            case 's':
            case 'S':
                this.solveCube();
                break;
            case 'c':
            case 'C':
                this.resetCamera();
                break;
            case 't':
            case 'T':
                this.setTopView();
                break;
            case 'f':
            case 'F':
                this.setFrontView();
                break;
        }
    }
    
    resetCube() {
        this.cubeGroup.rotation.set(0, 0, 0);
        this.controls.reset();
    }
    
    randomRotate() {
        const randomRotation = () => {
            const axis = Math.floor(Math.random() * 3);
            const angle = (Math.PI / 2) * (Math.floor(Math.random() * 4));
            
            switch(axis) {
                case 0: // X-axis
                    this.cubeGroup.rotateX(angle);
                    break;
                case 1: // Y-axis
                    this.cubeGroup.rotateY(angle);
                    break;
                case 2: // Z-axis
                    this.cubeGroup.rotateZ(angle);
                    break;
            }
        };
        
        // Perform multiple random rotations
        for (let i = 0; i < 10; i++) {
            setTimeout(() => randomRotation(), i * 100);
        }
    }
    
    solveCube() {
        // Animate back to solved state
        const targetRotation = { x: 0, y: 0, z: 0 };
        const currentRotation = {
            x: this.cubeGroup.rotation.x,
            y: this.cubeGroup.rotation.y,
            z: this.cubeGroup.rotation.z
        };
        
        const animate = () => {
            const progress = 0.05;
            this.cubeGroup.rotation.x += (targetRotation.x - currentRotation.x) * progress;
            this.cubeGroup.rotation.y += (targetRotation.y - currentRotation.y) * progress;
            this.cubeGroup.rotation.z += (targetRotation.z - currentRotation.z) * progress;
            
            if (Math.abs(this.cubeGroup.rotation.x) > 0.01 || 
                Math.abs(this.cubeGroup.rotation.y) > 0.01 || 
                Math.abs(this.cubeGroup.rotation.z) > 0.01) {
                requestAnimationFrame(animate);
            } else {
                this.cubeGroup.rotation.set(0, 0, 0);
            }
        };
        
        animate();
    }
    
    resetCamera() {
        this.camera.position.set(this.initialCameraPosition.x, this.initialCameraPosition.y, this.initialCameraPosition.z);
        this.controls.reset();
    }
    
    setTopView() {
        this.camera.position.set(0, 10, 0);
        this.controls.target.set(0, 0, 0);
        this.controls.update();
    }
    
    setFrontView() {
        this.camera.position.set(0, 0, 10);
        this.controls.target.set(0, 0, 0);
        this.controls.update();
    }
    
    updateCubeSize() {
        this.cubeGroup.scale.set(this.cubeSize, this.cubeSize, this.cubeSize);
    }
    
    updateWireframe() {
        this.cubeGroup.children.forEach(cube => {
            cube.material.wireframe = this.wireframe;
        });
    }
    
    onWindowResize() {
        const width = window.innerWidth;
        const height = window.innerHeight;
        
        this.camera.aspect = width / height;
        this.camera.updateProjectionMatrix();
        this.renderer.setSize(width, height);
        
        // Adjust for mobile
        if (this.isMobile) {
            const canvasContainer = document.getElementById('canvas-container');
            canvasContainer.style.height = `${height - 200}px`;
        }
    }
    
    animate() {
        requestAnimationFrame(() => this.animate());
        
        // Update controls
        this.controls.update();
        
        // Render scene
        this.renderer.render(this.scene, this.camera);
    }
}

// Initialize the simulator when the page loads
document.addEventListener('DOMContentLoaded', () => {
    // Add loading indicator
    const loading = document.createElement('div');
    loading.className = 'loading';
    loading.textContent = 'Loading 3D Cube Simulator...';
    document.body.appendChild(loading);
    
    // Initialize simulator
    const simulator = new CubeSimulator();
    
    // Remove loading indicator
    setTimeout(() => {
        loading.remove();
    }, 1000);
    
    // Performance monitoring for mobile
    if (simulator.isMobile) {
        let frameCount = 0;
        let lastTime = performance.now();
        
        const checkPerformance = () => {
            frameCount++;
            const currentTime = performance.now();
            
            if (currentTime - lastTime >= 1000) {
                const fps = Math.round((frameCount * 1000) / (currentTime - lastTime));
                
                if (fps < 30) {
                    // Reduce quality for better performance
                    simulator.renderer.setPixelRatio(1);
                    simulator.renderer.shadowMap.enabled = false;
                }
                
                frameCount = 0;
                lastTime = currentTime;
            }
            
            requestAnimationFrame(checkPerformance);
        };
        
        checkPerformance();
    }
});

// Service Worker for offline support (optional)
if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        navigator.serviceWorker.register('/sw.js')
            .then(registration => console.log('SW registered'))
            .catch(error => console.log('SW registration failed'));
    });
}