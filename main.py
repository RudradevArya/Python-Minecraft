import math # always useful to have
import ctypes # needed to interact with python at a lower level
import pyglet

pyglet.options["shadow_window"] = False # no need for shadow window and also bcz may cause problem on some os
pyglet.options["debug_gl"] = False # makes things slow, so disable it

import pyglet.gl as gl

import shader
import matrix # import matrix.py file

vertex_positions = [ # 3d coordinates for each vertex for the desired shape
	## set the Z component to 0.0 so that our object is centered
	-0.5,  0.5, 0.0,
	-0.5, -0.5, 0.0,
	 0.5, -0.5, 0.0,
	 0.5,  0.5, 0.0,
]

indices = [
	0, 1, 2, # first triangle
	0, 2, 3, # second triangle
]

'''
group of 3 indices makes a triangle
and 
one index points to each vertex positions

therfore creating 2 set of indices we are making 2 traingles into one square/rectangle
'''

class Window(pyglet.window.Window): # create a class extending pyglet.window.Window
	def __init__(self, **args): #**args means all the argumenats are passed ot this function
		super().__init__(**args) # pass on arguments to pyglet.window.Window.__init__ function
		
		# creating vertex array object (VAOs) which holds VBOs
		#https://stackoverflow.com/questions/23314787/use-of-vertex-array-objects-and-vertex-buffer-objects

		self.vao = gl.GLuint(0)
		gl.glGenVertexArrays(1, ctypes.byref(self.vao))
		gl.glBindVertexArray(self.vao)

		# creating vertex buffer object(VBOs)
		#https://stackoverflow.com/questions/23314787/use-of-vertex-array-objects-and-vertex-buffer-objects

		self.vbo = gl.GLuint(0)
		gl.glGenBuffers(1, ctypes.byref(self.vbo))
		gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.vbo)
		
		gl.glBufferData(gl.GL_ARRAY_BUFFER,
			ctypes.sizeof(gl.GLfloat * len(vertex_positions)),
			(gl.GLfloat * len(vertex_positions)) (*vertex_positions),
			gl.GL_STATIC_DRAW)
		
		gl.glVertexAttribPointer(0, 3, gl.GL_FLOAT, gl.GL_FALSE, 0, 0)
		gl.glEnableVertexAttribArray(0)

		# create index buffer object (IBOs) whichs contains all the indices 
		# https://openglbook.com/chapter-3-index-buffer-objects-and-primitive-types.html

		self.ibo = gl.GLuint(0)
		gl.glGenBuffers(1, self.ibo)
		gl.glBindBuffer(gl.GL_ELEMENT_ARRAY_BUFFER, self.ibo)

		gl.glBufferData(gl.GL_ELEMENT_ARRAY_BUFFER,
			ctypes.sizeof(gl.GLuint * len(indices)),
			(gl.GLuint * len(indices)) (*indices),
			gl.GL_STATIC_DRAW)
		
		# creating shader

		self.shader = shader.Shader("vert.glsl", "frag.glsl")
		self.shader_matrix_location = self.shader.find_uniform(b"matrix") # get the shader matrix uniform location
		self.shader.use()

		# create matrices

		self.mv_matrix = matrix.Matrix() # modelview
		self.p_matrix = matrix.Matrix() # projection

		self.x = 0 # temporary variable
		pyglet.clock.schedule_interval(self.update, 1.0 / 60) # call update function every 60th of a second
	
	def update(self, delta_time):
		self.x += delta_time # increment self.x consistently

	def on_draw(self):

		# create projection matrix
		#identity matrix is a spexial "neutral matrix" wheich when multiplied with vector wont be transformed
		self.p_matrix.load_identity()
		self.p_matrix.perspective(90, float(self.width) / self.height, 0.1, 500) #0.1 and 500 are the min and max distances of frustum

		# create model view matrix

		self.mv_matrix.load_identity()
		self.mv_matrix.translate(0, 0, -1)
		self.mv_matrix.rotate_2d(self.x + 6.28 / 4, math.sin(self.x / 3 * 2) / 2)

		# multiply the two matrices together and send to the shader program
		#making model view projection matrix
		mvp_matrix = self.p_matrix * self.mv_matrix
		self.shader.uniform_matrix(self.shader_matrix_location, mvp_matrix)

		#draw stuff
		gl.glClearColor(1.0, 0.5, 1.0, 1.0) # set clear colour
		self.clear() # clear screen
		gl.glDrawElements(gl.GL_TRIANGLES, len(indices), gl.GL_UNSIGNED_INT, None) # draw bound buffers to the screen
		
	def on_resize(self, width, height):
		print(f"Resize {width} * {height}") # print out window size, changed from older syntax
		gl.glViewport(0, 0, width, height) # resize the actual OpenGL viewport

class Game:
	def __init__(self):
		self.config = gl.Config(double_buffer = True, major_version = 3, minor_version = 3) # use modern opengl
		self.window = Window(config = self.config, width = 800, height = 600, caption = "Sasta Minecraft", resizable = True, vsync = False) # vsync with pyglet causes problems on some computers, so disable it
	
	def run(self):
		pyglet.app.run() # run our application

if __name__ == "__main__": # only run the game if source file is the one run
	game = Game() # create game object
	game.run()
