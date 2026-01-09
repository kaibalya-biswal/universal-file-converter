const canvas = document.getElementById('networkCanvas');
if (canvas) {
    const ctx = canvas.getContext('2d');
    let nodes = [];
    let connections = [];
    let animationId;

    function resizeCanvas() {
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
        initNetwork();
    }

    function initNetwork() {
        nodes = [];
        connections = [];
        
        const nodeCount = 30;
        const connectionDistance = 200;
        
        for (let i = 0; i < nodeCount; i++) {
            nodes.push({
                x: Math.random() * canvas.width,
                y: Math.random() * canvas.height,
                vx: (Math.random() - 0.5) * 0.5,
                vy: (Math.random() - 0.5) * 0.5,
                radius: Math.random() * 3 + 2,
                glow: Math.random() * 0.5 + 0.5
            });
        }
        
        for (let i = 0; i < nodes.length; i++) {
            for (let j = i + 1; j < nodes.length; j++) {
                const dx = nodes[i].x - nodes[j].x;
                const dy = nodes[i].y - nodes[j].y;
                const distance = Math.sqrt(dx * dx + dy * dy);
                
                if (distance < connectionDistance) {
                    connections.push({
                        node1: i,
                        node2: j,
                        distance: distance,
                        opacity: 1 - (distance / connectionDistance)
                    });
                }
            }
        }
    }

    function updateNodes() {
        nodes.forEach(node => {
            node.x += node.vx;
            node.y += node.vy;
            
            if (node.x < 0 || node.x > canvas.width) node.vx *= -1;
            if (node.y < 0 || node.y > canvas.height) node.vy *= -1;
            
            node.x = Math.max(0, Math.min(canvas.width, node.x));
            node.y = Math.max(0, Math.min(canvas.height, node.y));
            
            node.glow += (Math.random() - 0.5) * 0.1;
            node.glow = Math.max(0.3, Math.min(1, node.glow));
        });
    }

    function drawNetwork() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        
        connections.forEach(conn => {
            const node1 = nodes[conn.node1];
            const node2 = nodes[conn.node2];
            
            ctx.beginPath();
            ctx.moveTo(node1.x, node1.y);
            ctx.lineTo(node2.x, node2.y);
            ctx.strokeStyle = `rgba(255, 255, 255, ${conn.opacity * 0.1})`;
            ctx.lineWidth = 1;
            ctx.stroke();
        });
        
        nodes.forEach(node => {
            ctx.beginPath();
            ctx.arc(node.x, node.y, node.radius, 0, Math.PI * 2);
            
            const gradient = ctx.createRadialGradient(
                node.x, node.y, 0,
                node.x, node.y, node.radius * 3
            );
            gradient.addColorStop(0, `rgba(255, 255, 255, ${node.glow})`);
            gradient.addColorStop(1, 'rgba(255, 255, 255, 0)');
            
            ctx.fillStyle = gradient;
            ctx.fill();
            
            ctx.fillStyle = `rgba(255, 255, 255, ${node.glow * 0.8})`;
            ctx.fill();
        });
    }

    function animate() {
        updateNodes();
        drawNetwork();
        animationId = requestAnimationFrame(animate);
    }

    resizeCanvas();
    window.addEventListener('resize', resizeCanvas);
    animate();
}
