// Stat Node Positioning System - Prevents overlap with text content

(function() {
    'use strict';

    const statNodes = document.querySelectorAll('.stat-node');
    const heroSection = document.querySelector('.hero-section');
    const contentContainer = document.querySelector('.content-container');
    
    if (statNodes.length === 0) return;

    // Get bounding boxes of text elements
    function getTextElements() {
        const elements = [];
        
        if (heroSection) {
            const heroText = heroSection.querySelectorAll('h1, h2, h3, p, .hero-headline, .hero-subtitle, .hero-actions');
            heroText.forEach(el => {
                const rect = el.getBoundingClientRect();
                if (rect.width > 0 && rect.height > 0) {
                    elements.push({
                        left: rect.left,
                        top: rect.top,
                        right: rect.right,
                        bottom: rect.bottom,
                        width: rect.width,
                        height: rect.height
                    });
                }
            });
        }
        
        if (contentContainer) {
            const contentRect = contentContainer.getBoundingClientRect();
            if (contentRect.width > 0 && contentRect.height > 0) {
                elements.push({
                    left: contentRect.left,
                    top: contentRect.top,
                    right: contentRect.right,
                    bottom: contentRect.bottom,
                    width: contentRect.width,
                    height: contentRect.height
                });
            }
        }
        
        return elements;
    }

    // Check if a position overlaps with text elements
    function checkOverlap(nodeRect, textElements, padding = 20) {
        for (const textRect of textElements) {
            if (
                nodeRect.left < textRect.right + padding &&
                nodeRect.right > textRect.left - padding &&
                nodeRect.top < textRect.bottom + padding &&
                nodeRect.bottom > textRect.top - padding
            ) {
                return true;
            }
        }
        return false;
    }

    // Calculate node rectangle from position
    function calculateNodeRect(pos, viewportWidth, viewportHeight) {
        const nodeWidth = 150;
        const nodeHeight = 100;
        
        let nodeRect;
        if (pos.top !== undefined && pos.left !== undefined) {
            const top = (parseFloat(pos.top) / 100) * viewportHeight;
            const left = (parseFloat(pos.left) / 100) * viewportWidth;
            nodeRect = {
                left: left,
                top: top,
                right: left + nodeWidth,
                bottom: top + nodeHeight
            };
        } else if (pos.top !== undefined && pos.right !== undefined) {
            const top = (parseFloat(pos.top) / 100) * viewportHeight;
            const right = (parseFloat(pos.right) / 100) * viewportWidth;
            nodeRect = {
                left: viewportWidth - right - nodeWidth,
                top: top,
                right: viewportWidth - right,
                bottom: top + nodeHeight
            };
        } else if (pos.bottom !== undefined && pos.left !== undefined) {
            const bottom = (parseFloat(pos.bottom) / 100) * viewportHeight;
            const left = (parseFloat(pos.left) / 100) * viewportWidth;
            nodeRect = {
                left: left,
                top: viewportHeight - bottom - nodeHeight,
                right: left + nodeWidth,
                bottom: viewportHeight - bottom
            };
        } else if (pos.bottom !== undefined && pos.right !== undefined) {
            const bottom = (parseFloat(pos.bottom) / 100) * viewportHeight;
            const right = (parseFloat(pos.right) / 100) * viewportWidth;
            nodeRect = {
                left: viewportWidth - right - nodeWidth,
                top: viewportHeight - bottom - nodeHeight,
                right: viewportWidth - right,
                bottom: viewportHeight - bottom
            };
        }
        return nodeRect;
    }

    // Find a free position for a stat node
    function findFreePosition(node, textElements, viewportWidth, viewportHeight, nodeIndex) {
        const nodeWidth = 150; // Approximate width
        const nodeHeight = 100; // Approximate height
        const padding = 20;
        
        // Define positions for each stat node to distribute them across left and right
        const nodePositions = [
            // Node 0: Top-left
            [
                { top: '8%', left: '2%' },
                { top: '12%', left: '1%' },
                { top: '5%', left: '3%' },
                { top: '15%', left: '2%' },
                { top: '20%', left: '1%' }
            ],
            // Node 1: Bottom-left
            [
                { bottom: '15%', left: '2%' },
                { bottom: '20%', left: '1%' },
                { bottom: '12%', left: '3%' },
                { bottom: '25%', left: '2%' },
                { bottom: '30%', left: '1%' }
            ],
            // Node 2: Top-right
            [
                { top: '8%', right: '2%' },
                { top: '12%', right: '1%' },
                { top: '5%', right: '3%' },
                { top: '15%', right: '2%' },
                { top: '20%', right: '1%' }
            ],
            // Node 3: Bottom-right
            [
                { bottom: '15%', right: '2%' },
                { bottom: '20%', right: '1%' },
                { bottom: '12%', right: '3%' },
                { bottom: '25%', right: '2%' },
                { bottom: '30%', right: '1%' }
            ]
        ];

        // Get positions for this specific node
        const positions = nodePositions[nodeIndex] || nodePositions[0];

        for (const pos of positions) {
            const nodeRect = calculateNodeRect(pos, viewportWidth, viewportHeight);
            if (nodeRect && !checkOverlap(nodeRect, textElements, padding)) {
                return pos;
            }
        }

        // Fallback: return a safe corner position
        return { top: '5%', right: '2%' };
    }

    // Position all stat nodes
    function positionStatNodes() {
        if (window.innerWidth < 1200) {
            statNodes.forEach(node => {
                node.style.display = 'none';
            });
            return;
        }

        statNodes.forEach(node => {
            node.style.display = 'block';
        });

        const textElements = getTextElements();
        const viewportWidth = window.innerWidth;
        const viewportHeight = window.innerHeight;

        // Store used positions to avoid duplicates
        const usedPositions = [];

        // Generate unique positions for each of the 4 tiles with different strategies
        
        statNodes.forEach((node, index) => {
            let position;
            let attempts = 0;
            const maxAttempts = 50;
            
            do {
                // Different positioning strategy for each of the 4 tiles
                switch(index) {
                    case 0: // First tile - Top-left corner area, higher up
                        const top1 = 5 + Math.random() * 15; // 5% to 20%
                        const left1 = 1.5 + Math.random() * 2.5; // 1.5% to 4%
                        position = { top: `${top1.toFixed(1)}%`, left: `${left1.toFixed(1)}%` };
                        break;
                        
                    case 1: // Second tile - Bottom-left area, lower down
                        const bottom1 = 12 + Math.random() * 25; // 12% to 37%
                        const left2 = 1 + Math.random() * 2; // 1% to 3%
                        position = { bottom: `${bottom1.toFixed(1)}%`, left: `${left2.toFixed(1)}%` };
                        break;
                        
                    case 2: // Third tile - Top-right corner area, middle-high
                        const top2 = 8 + Math.random() * 20; // 8% to 28%
                        const right1 = 1.5 + Math.random() * 2.5; // 1.5% to 4%
                        position = { top: `${top2.toFixed(1)}%`, right: `${right1.toFixed(1)}%` };
                        break;
                        
                    case 3: // Fourth tile - Bottom-right area, varied height
                        const bottom2 = 15 + Math.random() * 20; // 15% to 35%
                        const right2 = 1 + Math.random() * 3; // 1% to 4%
                        position = { bottom: `${bottom2.toFixed(1)}%`, right: `${right2.toFixed(1)}%` };
                        break;
                        
                    default:
                        // Fallback for any additional nodes
                        const topFallback = 10 + Math.random() * 30;
                        const side = Math.random() > 0.5 ? 'left' : 'right';
                        if (side === 'left') {
                            position = { top: `${topFallback.toFixed(1)}%`, left: '2%' };
                        } else {
                            position = { top: `${topFallback.toFixed(1)}%`, right: '2%' };
                        }
                }
                
                // Check for overlap with text
                const nodeRect = calculateNodeRect(position, viewportWidth, viewportHeight);
                const overlapsText = checkOverlap(nodeRect, textElements, 20);
                
                // Check for overlap with other stat nodes
                const positionKey = JSON.stringify(position);
                const overlapsOther = usedPositions.some(usedPos => {
                    const usedRect = calculateNodeRect(JSON.parse(usedPos), viewportWidth, viewportHeight);
                    if (!usedRect) return false;
                    return checkOverlap(nodeRect, [usedRect], 10);
                });
                
                if (!overlapsText && !overlapsOther) {
                    usedPositions.push(positionKey);
                    break;
                }
                
                attempts++;
            } while (attempts < maxAttempts);
            
            // Fallback to safe position if no random position found
            if (attempts >= maxAttempts) {
                const fallbackPositions = [
                    { top: '8%', left: '2%' },      // Tile 0
                    { bottom: '15%', left: '2%' },  // Tile 1
                    { top: '10%', right: '2%' },    // Tile 2
                    { bottom: '18%', right: '2%' }  // Tile 3
                ];
                position = fallbackPositions[index] || fallbackPositions[0];
            }

            // Apply position
            Object.keys(position).forEach(key => {
                node.style[key] = position[key];
            });

            // Remove old positioning classes
            node.className = node.className.replace(/stat-node-\w+-\w+/g, '');
            node.className = node.className.trim() + ' stat-node';
        });
    }

    // Initialize on page load
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', () => {
            setTimeout(positionStatNodes, 100);
        });
    } else {
        setTimeout(positionStatNodes, 100);
    }

    // Reposition on window resize
    let resizeTimeout;
    window.addEventListener('resize', () => {
        clearTimeout(resizeTimeout);
        resizeTimeout = setTimeout(positionStatNodes, 250);
    });

    // Reposition on scroll (in case content changes)
    let scrollTimeout;
    window.addEventListener('scroll', () => {
        clearTimeout(scrollTimeout);
        scrollTimeout = setTimeout(positionStatNodes, 250);
    });

    // Reposition when content changes (using MutationObserver)
    const observer = new MutationObserver(() => {
        setTimeout(positionStatNodes, 100);
    });

    if (heroSection) {
        observer.observe(heroSection, { childList: true, subtree: true, attributes: true });
    }
    if (contentContainer) {
        observer.observe(contentContainer, { childList: true, subtree: true, attributes: true });
    }

})();
