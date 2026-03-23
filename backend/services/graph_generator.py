# import matplotlib
# matplotlib.use('Agg')  # Non-interactive backend
# import matplotlib.pyplot as plt
# import numpy as np
# import sympy as sp
# import re
# from pathlib import Path

# class GraphGenerator:
#     def __init__(self):
#         self.output_dir = Path("temp/graphs")
#         self.output_dir.mkdir(parents=True, exist_ok=True)
    
#     def generate_graph_from_equation(self, equation: str, output_filename: str) -> str:
#         """Generate graph from mathematical equation"""
        
#         try:
#             print(f"📊 Generating graph for: {equation}")
            
#             # Detect equation type
#             if self._is_quadratic(equation):
#                 return self._plot_quadratic(equation, output_filename)
#             elif self._is_linear(equation):
#                 return self._plot_linear(equation, output_filename)
#             elif self._has_trig(equation):
#                 return self._plot_trigonometric(equation, output_filename)
#             else:
#                 return self._plot_general(equation, output_filename)
                
#         except Exception as e:
#             print(f"❌ Graph generation error: {e}")
#             return None
    
#     def _is_quadratic(self, eq: str) -> bool:
#         """Check if equation is quadratic"""
#         return 'x²' in eq or 'x^2' in eq or 'x**2' in eq
    
#     def _is_linear(self, eq: str) -> bool:
#         """Check if equation is linear"""
#         return ('=' in eq and 'x' in eq and 
#                 'x²' not in eq and 'x^2' not in eq)
    
#     def _has_trig(self, eq: str) -> bool:
#         """Check if has trigonometric functions"""
#         return any(fn in eq.lower() for fn in ['sin', 'cos', 'tan'])
    
#     def _plot_quadratic(self, equation: str, filename: str) -> str:
#         """Plot quadratic equation"""
        
#         # Parse coefficients (simplified)
#         # e.g., "x² + 2x + 1 = 0"
        
#         fig, ax = plt.subplots(figsize=(10, 6))
        
#         # Generate parabola
#         x = np.linspace(-10, 10, 400)
#         y = x**2  # Simplified
        
#         ax.plot(x, y, 'b-', linewidth=2, label='y = x²')
#         ax.axhline(y=0, color='k', linewidth=0.5)
#         ax.axvline(x=0, color='k', linewidth=0.5)
#         ax.grid(True, alpha=0.3)
#         ax.set_xlabel('x', fontsize=14)
#         ax.set_ylabel('y', fontsize=14)
#         ax.set_title('Quadratic Function', fontsize=16, fontweight='bold')
#         ax.legend(fontsize=12)
        
#         output_path = self.output_dir / filename
#         plt.savefig(output_path, dpi=150, bbox_inches='tight')
#         plt.close()
        
#         print(f"✅ Graph saved: {output_path}")
#         return str(output_path)
    
#     def _plot_linear(self, equation: str, filename: str) -> str:
#         """Plot linear equation"""
        
#         fig, ax = plt.subplots(figsize=(10, 6))
        
#         x = np.linspace(-10, 10, 100)
#         y = 2*x + 3  # Simplified
        
#         ax.plot(x, y, 'r-', linewidth=2, label='y = 2x + 3')
#         ax.axhline(y=0, color='k', linewidth=0.5)
#         ax.axvline(x=0, color='k', linewidth=0.5)
#         ax.grid(True, alpha=0.3)
#         ax.set_xlabel('x', fontsize=14)
#         ax.set_ylabel('y', fontsize=14)
#         ax.set_title('Linear Function', fontsize=16, fontweight='bold')
#         ax.legend(fontsize=12)
        
#         output_path = self.output_dir / filename
#         plt.savefig(output_path, dpi=150, bbox_inches='tight')
#         plt.close()
        
#         return str(output_path)
    
#     def _plot_trigonometric(self, equation: str, filename: str) -> str:
#         """Plot trigonometric function"""
        
#         fig, ax = plt.subplots(figsize=(10, 6))
        
#         x = np.linspace(-2*np.pi, 2*np.pi, 400)
        
#         if 'sin' in equation.lower():
#             y = np.sin(x)
#             label = 'y = sin(x)'
#         elif 'cos' in equation.lower():
#             y = np.cos(x)
#             label = 'y = cos(x)'
#         else:
#             y = np.tan(x)
#             label = 'y = tan(x)'
        
#         ax.plot(x, y, 'g-', linewidth=2, label=label)
#         ax.axhline(y=0, color='k', linewidth=0.5)
#         ax.axvline(x=0, color='k', linewidth=0.5)
#         ax.grid(True, alpha=0.3)
#         ax.set_xlabel('x', fontsize=14)
#         ax.set_ylabel('y', fontsize=14)
#         ax.set_title('Trigonometric Function', fontsize=16, fontweight='bold')
#         ax.legend(fontsize=12)
#         ax.set_ylim(-2, 2)
        
#         output_path = self.output_dir / filename
#         plt.savefig(output_path, dpi=150, bbox_inches='tight')
#         plt.close()
        
#         return str(output_path)
    
#     def _plot_general(self, equation: str, filename: str) -> str:
#         """Plot general mathematical concept"""
        
#         fig, ax = plt.subplots(figsize=(10, 6))
        
#         # Create a simple visualization
#         x = np.linspace(0, 10, 100)
#         y = np.exp(-x/3) * np.sin(x)
        
#         ax.plot(x, y, 'purple', linewidth=2)
#         ax.grid(True, alpha=0.3)
#         ax.set_title('Mathematical Function', fontsize=16, fontweight='bold')
        
#         output_path = self.output_dir / filename
#         plt.savefig(output_path, dpi=150, bbox_inches='tight')
#         plt.close()
        
#         return str(output_path)

# graph_generator = GraphGenerator()














import matplotlib
matplotlib.use('Agg')  # Non-GUI backend
import matplotlib.pyplot as plt
import numpy as np
import os
import re

class GraphGenerator:
    """Generate graphs for math formulas and examples"""
    
    def __init__(self):
        self.output_dir = "temp/graphs"
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Set style
        plt.style.use('seaborn-v0_8-darkgrid')
    
    def detect_and_generate_graph(self, content):
        """
        Auto-detect if content needs a graph and generate it
        Returns: graph_path or None
        """
        
        # Check for common math topics that need graphs
        math_keywords = {
            'quadratic': self.plot_quadratic,
            'linear equation': self.plot_linear,
            'sine': self.plot_sine,
            'cosine': self.plot_cosine,
            'exponential': self.plot_exponential,
            'parabola': self.plot_parabola,
            'circle': self.plot_circle,
            'slope': self.plot_slope,
        }
        
        content_lower = content.lower()
        
        for keyword, plot_function in math_keywords.items():
            if keyword in content_lower:
                print(f"📊 Generating graph for: {keyword}")
                return plot_function()
        
        return None
    
    def plot_quadratic(self):
        """Plot y = ax² + bx + c"""
        fig, ax = plt.subplots(figsize=(10, 6))
        
        x = np.linspace(-5, 5, 100)
        
        # Multiple quadratics
        y1 = x**2
        y2 = -x**2 + 4
        y3 = 2*x**2 - 3*x + 1
        
        ax.plot(x, y1, label='y = x²', linewidth=2)
        ax.plot(x, y2, label='y = -x² + 4', linewidth=2)
        ax.plot(x, y3, label='y = 2x² - 3x + 1', linewidth=2)
        
        ax.axhline(y=0, color='k', linewidth=0.5)
        ax.axvline(x=0, color='k', linewidth=0.5)
        ax.grid(True, alpha=0.3)
        ax.legend(fontsize=12)
        ax.set_xlabel('x', fontsize=14)
        ax.set_ylabel('y', fontsize=14)
        ax.set_title('Quadratic Functions', fontsize=16, fontweight='bold')
        
        filepath = f"{self.output_dir}/quadratic_{int(np.random.random()*1000)}.png"
        plt.savefig(filepath, dpi=150, bbox_inches='tight')
        plt.close()
        
        return filepath
    
    def plot_linear(self):
        """Plot y = mx + c"""
        fig, ax = plt.subplots(figsize=(10, 6))
        
        x = np.linspace(-5, 5, 100)
        
        # Different slopes
        y1 = 2*x + 1
        y2 = -x + 3
        y3 = 0.5*x - 2
        
        ax.plot(x, y1, label='y = 2x + 1 (m=2)', linewidth=2)
        ax.plot(x, y2, label='y = -x + 3 (m=-1)', linewidth=2)
        ax.plot(x, y3, label='y = 0.5x - 2 (m=0.5)', linewidth=2)
        
        ax.axhline(y=0, color='k', linewidth=0.5)
        ax.axvline(x=0, color='k', linewidth=0.5)
        ax.grid(True, alpha=0.3)
        ax.legend(fontsize=12)
        ax.set_xlabel('x', fontsize=14)
        ax.set_ylabel('y', fontsize=14)
        ax.set_title('Linear Equations (Slope-Intercept Form)', fontsize=16, fontweight='bold')
        
        filepath = f"{self.output_dir}/linear_{int(np.random.random()*1000)}.png"
        plt.savefig(filepath, dpi=150, bbox_inches='tight')
        plt.close()
        
        return filepath
    
    def plot_sine(self):
        """Plot sine wave"""
        fig, ax = plt.subplots(figsize=(12, 6))
        
        x = np.linspace(0, 4*np.pi, 1000)
        y = np.sin(x)
        
        ax.plot(x, y, linewidth=2.5, color='#2E86AB')
        ax.axhline(y=0, color='k', linewidth=0.5)
        ax.grid(True, alpha=0.3)
        
        # Mark key points
        key_x = [0, np.pi/2, np.pi, 3*np.pi/2, 2*np.pi]
        key_y = [0, 1, 0, -1, 0]
        ax.scatter(key_x, key_y, color='red', s=100, zorder=5)
        
        ax.set_xlabel('x (radians)', fontsize=14)
        ax.set_ylabel('sin(x)', fontsize=14)
        ax.set_title('Sine Function: y = sin(x)', fontsize=16, fontweight='bold')
        ax.set_xticks([0, np.pi/2, np.pi, 3*np.pi/2, 2*np.pi, 5*np.pi/2, 3*np.pi, 7*np.pi/2, 4*np.pi])
        ax.set_xticklabels(['0', 'π/2', 'π', '3π/2', '2π', '5π/2', '3π', '7π/2', '4π'])
        
        filepath = f"{self.output_dir}/sine_{int(np.random.random()*1000)}.png"
        plt.savefig(filepath, dpi=150, bbox_inches='tight')
        plt.close()
        
        return filepath
    
    def plot_exponential(self):
        """Plot exponential growth"""
        fig, ax = plt.subplots(figsize=(10, 6))
        
        x = np.linspace(-2, 3, 100)
        
        y1 = np.exp(x)
        y2 = 2**x
        y3 = np.exp(-x)
        
        ax.plot(x, y1, label='y = eˣ', linewidth=2)
        ax.plot(x, y2, label='y = 2ˣ', linewidth=2)
        ax.plot(x, y3, label='y = e⁻ˣ (decay)', linewidth=2, linestyle='--')
        
        ax.axhline(y=0, color='k', linewidth=0.5)
        ax.axvline(x=0, color='k', linewidth=0.5)
        ax.grid(True, alpha=0.3)
        ax.legend(fontsize=12)
        ax.set_xlabel('x', fontsize=14)
        ax.set_ylabel('y', fontsize=14)
        ax.set_title('Exponential Functions', fontsize=16, fontweight='bold')
        ax.set_ylim(0, 20)
        
        filepath = f"{self.output_dir}/exponential_{int(np.random.random()*1000)}.png"
        plt.savefig(filepath, dpi=150, bbox_inches='tight')
        plt.close()
        
        return filepath
    
    def plot_parabola(self):
        """Same as quadratic"""
        return self.plot_quadratic()
    
    def plot_cosine(self):
        """Plot cosine wave"""
        fig, ax = plt.subplots(figsize=(12, 6))
        
        x = np.linspace(0, 4*np.pi, 1000)
        y = np.cos(x)
        
        ax.plot(x, y, linewidth=2.5, color='#A23B72')
        ax.axhline(y=0, color='k', linewidth=0.5)
        ax.grid(True, alpha=0.3)
        
        ax.set_xlabel('x (radians)', fontsize=14)
        ax.set_ylabel('cos(x)', fontsize=14)
        ax.set_title('Cosine Function: y = cos(x)', fontsize=16, fontweight='bold')
        ax.set_xticks([0, np.pi/2, np.pi, 3*np.pi/2, 2*np.pi, 5*np.pi/2, 3*np.pi, 7*np.pi/2, 4*np.pi])
        ax.set_xticklabels(['0', 'π/2', 'π', '3π/2', '2π', '5π/2', '3π', '7π/2', '4π'])
        
        filepath = f"{self.output_dir}/cosine_{int(np.random.random()*1000)}.png"
        plt.savefig(filepath, dpi=150, bbox_inches='tight')
        plt.close()
        
        return filepath
    
    def plot_circle(self):
        """Plot circle equation"""
        fig, ax = plt.subplots(figsize=(8, 8))
        
        theta = np.linspace(0, 2*np.pi, 1000)
        
        # x² + y² = r²
        r = 3
        x = r * np.cos(theta)
        y = r * np.sin(theta)
        
        ax.plot(x, y, linewidth=3, color='#F18F01')
        ax.axhline(y=0, color='k', linewidth=0.5)
        ax.axvline(x=0, color='k', linewidth=0.5)
        ax.grid(True, alpha=0.3)
        
        # Mark center
        ax.scatter([0], [0], color='red', s=100, zorder=5, label='Center (0,0)')
        
        # Mark radius
        ax.plot([0, r], [0, 0], 'r--', linewidth=2, label=f'Radius = {r}')
        
        ax.set_xlabel('x', fontsize=14)
        ax.set_ylabel('y', fontsize=14)
        ax.set_title(f'Circle: x² + y² = {r}²', fontsize=16, fontweight='bold')
        ax.legend(fontsize=12)
        ax.set_aspect('equal')
        ax.set_xlim(-5, 5)
        ax.set_ylim(-5, 5)
        
        filepath = f"{self.output_dir}/circle_{int(np.random.random()*1000)}.png"
        plt.savefig(filepath, dpi=150, bbox_inches='tight')
        plt.close()
        
        return filepath
    
    def plot_slope(self):
        """Plot slope example"""
        return self.plot_linear()

graph_generator = GraphGenerator()