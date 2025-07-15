# 3D Cube Simulator

A modern, interactive 3D cube simulator built with Three.js that works seamlessly on both desktop and mobile browsers, including Android devices.

## 🌟 Features

### Interactive 3D Cube
- **Realistic 3D rendering** with WebGL
- **Smooth 60fps performance** optimized for mobile devices
- **Dynamic lighting** with ambient, directional, and point lights
- **Shadow mapping** for realistic depth perception

### Multiple Materials
- **Basic**: Standard phong material with transparency
- **Metal**: Metallic surface with high reflectivity
- **Glass**: Transparent material with refraction
- **Wood**: Natural wood texture with low shininess
- **Neon**: Glowing material with emissive properties

### Cross-Platform Controls
- **Desktop**: Mouse drag to rotate, scroll wheel to zoom
- **Mobile**: Touch swipe to rotate, pinch gestures to zoom
- **Auto-rotation**: Adjustable speed slider for continuous rotation
- **Reset view**: One-click reset to default position

### Mobile Optimizations
- **Touch-friendly UI** with proper touch targets (44px minimum)
- **Responsive design** that adapts to all screen sizes
- **Performance optimizations** for mobile GPUs
- **PWA support** for app-like experience

### Advanced Features
- **Fullscreen mode** for immersive experience
- **Real-time FPS counter** and performance metrics
- **Smooth interpolation** for fluid animations
- **Service Worker** for offline functionality

## 🚀 Getting Started

### Prerequisites
- Modern web browser with WebGL support
- No additional software installation required

### Installation
1. Clone or download the project files
2. Open `index.html` in a web browser
3. For best experience, serve via a local web server:
   ```bash
   # Using Python 3
   python -m http.server 8000
   
   # Using Node.js
   npx serve .
   
   # Using PHP
   php -S localhost:8000
   ```

### Usage
1. **Rotate the cube**: Drag with mouse or swipe on touch devices
2. **Zoom in/out**: Scroll wheel or pinch gestures
3. **Change materials**: Use the material dropdown
4. **Auto-rotation**: Adjust the rotation speed slider
5. **Reset view**: Click the "Reset View" button
6. **Fullscreen**: Click the "Fullscreen" button

## 📱 Mobile Support

### Android Browser Compatibility
- **Chrome for Android**: Full support with hardware acceleration
- **Samsung Internet**: Full support
- **Firefox for Android**: Full support
- **Opera Mobile**: Full support

### iOS Browser Compatibility
- **Safari**: Full support
- **Chrome for iOS**: Full support
- **Firefox for iOS**: Full support

### Performance Optimizations
- **WebGL hardware acceleration** detection
- **Adaptive pixel ratio** based on device capabilities
- **Touch event optimization** with passive listeners
- **Memory management** for long-running sessions

## 🛠️ Technical Details

### Technologies Used
- **Three.js r128**: 3D graphics library
- **WebGL**: Hardware-accelerated rendering
- **CSS3**: Modern styling with backdrop filters
- **ES6+**: Modern JavaScript features
- **Service Workers**: PWA capabilities

### Architecture
```
├── index.html          # Main HTML structure
├── styles.css          # Responsive CSS styling
├── script.js           # Three.js application logic
├── sw.js              # Service Worker for PWA
├── manifest.json      # Web App Manifest
└── README.md          # Project documentation
```

### Key Components
- **CubeSimulator Class**: Main application controller
- **Material System**: Dynamic material switching
- **Input Handler**: Cross-platform input management
- **Performance Monitor**: Real-time FPS tracking
- **Responsive UI**: Adaptive layout system

## 🎨 Customization

### Adding New Materials
```javascript
// In script.js, add to setupMaterials()
this.materials.custom = new THREE.MeshPhongMaterial({
    color: 0xyour_color,
    shininess: 100,
    // Add other properties as needed
});
```

### Modifying Controls
```javascript
// Adjust rotation sensitivity
this.targetRotationY += deltaX * 0.005; // Slower rotation
this.targetRotationY += deltaX * 0.02;  // Faster rotation
```

### Changing Colors
```css
/* In styles.css */
body {
    background: linear-gradient(135deg, #your_color1 0%, #your_color2 100%);
}
```

## 🔧 Development

### Local Development
1. Set up a local web server
2. Enable browser developer tools
3. Use device emulation for mobile testing
4. Monitor WebGL performance in dev tools

### Debugging
- Check browser console for WebGL errors
- Monitor FPS counter for performance issues
- Test touch events in device emulation mode
- Verify PWA installation on mobile devices

## 📊 Performance

### Target Performance
- **Desktop**: 60 FPS on modern hardware
- **Mobile**: 30-60 FPS depending on device
- **Memory**: <50MB RAM usage
- **Load time**: <2 seconds on 3G connection

### Optimization Techniques
- **Frustum culling** for off-screen objects
- **Level of detail** (LOD) system
- **Texture compression** and caching
- **Efficient geometry** with minimal vertices

## 🌐 Browser Support

### Required Features
- WebGL 1.0 or higher
- ES6+ JavaScript support
- Touch events (for mobile)
- Service Worker API (for PWA)

### Minimum Versions
- **Chrome**: 51+
- **Firefox**: 54+
- **Safari**: 10+
- **Edge**: 79+
- **Android Browser**: 5.0+

## 📄 License

This project is open source and available under the MIT License.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test on multiple devices
5. Submit a pull request

## 📞 Support

For issues or questions:
- Check browser compatibility
- Verify WebGL support
- Test on different devices
- Review console for errors

---

**Built with ❤️ for the web and mobile experience**