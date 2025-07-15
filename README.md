# 3D Cube Simulator

A modern, responsive web-based 3D cube simulator built with Three.js that works seamlessly on both desktop and mobile browsers, including Android devices.

## 🌟 Features

### Core Functionality
- **Interactive 3D Cube**: Rotate, zoom, and pan around a 3D cube structure
- **Rubik's Cube Style**: 3x3x3 cube structure with colored faces
- **Auto-rotation**: Smooth automatic rotation with adjustable speed
- **Multiple Views**: Top view, front view, and free camera control

### Mobile Optimization
- **Touch Controls**: Intuitive touch gestures for mobile devices
- **Responsive Design**: Adapts to different screen sizes
- **Performance Optimized**: Automatic quality adjustment for mobile devices
- **Android Browser Support**: Fully compatible with Android browsers

### Interactive Controls
- **Cube Manipulation**: Reset, random rotation, and solve functions
- **Camera Controls**: Reset camera position and preset views
- **Visual Options**: Adjustable cube size, rotation speed, and wireframe mode
- **Keyboard Shortcuts**: Quick access to all functions

## 🚀 Quick Start

1. **Clone or Download** the project files
2. **Open** `index.html` in any modern web browser
3. **Enjoy** the 3D cube simulator!

No installation or build process required - it's ready to run immediately.

## 📱 Mobile Usage

### Touch Controls
- **Single Finger Drag**: Rotate the camera around the cube
- **Two Finger Pinch**: Zoom in and out
- **Double Tap**: Reset the cube to its original position
- **Swipe Up/Down**: Show/hide the control panel (mobile only)

### Mobile-Specific Features
- **Floating Action Buttons**: Quick access to main functions
- **Collapsible Controls**: Slide-up control panel to save screen space
- **Performance Monitoring**: Automatic quality adjustment for smooth performance
- **Touch-Optimized UI**: Larger buttons and touch-friendly interface

## 🎮 Controls

### Desktop Controls
- **Mouse Drag**: Rotate camera
- **Mouse Wheel**: Zoom in/out
- **Right Click + Drag**: Pan camera

### Keyboard Shortcuts
- **R**: Reset cube
- **Space**: Random rotation
- **S**: Solve cube
- **C**: Reset camera
- **T**: Top view
- **F**: Front view

### Touch Controls (Mobile)
- **Drag**: Rotate camera
- **Pinch**: Zoom
- **Double Tap**: Reset cube
- **Swipe Up**: Show controls
- **Swipe Down**: Hide controls

## 🛠️ Technical Details

### Technologies Used
- **Three.js**: 3D graphics rendering
- **WebGL**: Hardware-accelerated graphics
- **HTML5 Canvas**: Cross-platform compatibility
- **CSS3**: Responsive design and animations
- **Vanilla JavaScript**: No framework dependencies

### Browser Compatibility
- **Desktop**: Chrome, Firefox, Safari, Edge
- **Mobile**: Chrome Mobile, Firefox Mobile, Safari Mobile
- **Android**: All modern Android browsers
- **iOS**: Safari and Chrome for iOS

### Performance Features
- **Adaptive Quality**: Automatically adjusts rendering quality based on device performance
- **Efficient Rendering**: Optimized for 60fps on most devices
- **Memory Management**: Proper cleanup and resource management
- **Mobile Optimization**: Reduced shadow maps and pixel ratio for mobile devices

## 📁 Project Structure

```
3d-cube-simulator/
├── index.html          # Main HTML file
├── styles.css          # Responsive CSS styles
├── script.js           # Main JavaScript application
└── README.md           # This file
```

## 🎨 Customization

### Modifying the Cube
- **Colors**: Edit the `colors` array in `script.js`
- **Size**: Adjust `cubeSize` and `gap` variables
- **Materials**: Modify material properties in `createCube()`

### Adding Features
- **New Controls**: Add event listeners in `setupEventListeners()`
- **Animations**: Extend the animation system in the `animate()` method
- **Effects**: Add post-processing effects to the renderer

## 🔧 Development

### Local Development
1. Clone the repository
2. Open `index.html` in a local web server (recommended)
3. Use browser developer tools for debugging

### Testing on Mobile
1. Use browser developer tools device emulation
2. Test on actual mobile devices
3. Use tools like BrowserStack for cross-device testing

## 🌐 Deployment

### Static Hosting
- **GitHub Pages**: Push to a GitHub repository and enable Pages
- **Netlify**: Drag and drop the folder to Netlify
- **Vercel**: Connect your repository to Vercel
- **Any Web Server**: Upload files to any web hosting service

### HTTPS Requirement
Modern browsers require HTTPS for WebGL features. Ensure your hosting supports HTTPS.

## 📊 Performance Tips

### For Developers
- **Reduce Geometry**: Use fewer polygons for mobile devices
- **Optimize Textures**: Use compressed textures and appropriate sizes
- **Limit Lights**: Reduce the number of light sources on mobile
- **Use LOD**: Implement Level of Detail for complex scenes

### For Users
- **Close Other Tabs**: Free up memory for better performance
- **Update Browser**: Use the latest browser version
- **Enable Hardware Acceleration**: Ensure WebGL is enabled

## 🤝 Contributing

Feel free to contribute to this project by:
- Reporting bugs
- Suggesting new features
- Improving performance
- Adding new cube types or animations
- Enhancing mobile experience

## 📄 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- **Three.js Community**: For the excellent 3D library
- **WebGL**: For hardware-accelerated graphics
- **Modern Web Standards**: For cross-platform compatibility

---

**Enjoy exploring the 3D cube simulator!** 🎲✨