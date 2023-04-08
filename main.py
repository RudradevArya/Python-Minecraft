import math # always useful to have
import ctypes # needed to interact with python at a lower level
import pyglet

pyglet.options["shadow_window"] = False # no need for shadow window and also bcz may cause problem on some os
pyglet.options["debug_gl"] = False # makes things slow, so disable it

import pyglet.gl as gl

import shader
import matrix # import matrix.py file
import block_type
import texture_manager
import camera



class Window(pyglet.window.Window): # create a class extending pyglet.window.Window
	def __init__(self, **args): #**args means all the argumenats are passed ot this function
		super().__init__(**args) # pass on arguments to pyglet.window.Window.__init__ function
		
		# create blocks

		self.texture_manager = texture_manager.Texture_manager(16, 16, 256) # create our texture manager (256 textures that are 16 x 16 pixels each)

		self.cobblestone = block_type.Block_type(self.texture_manager, "cobblestone", {"all": "cobblestone"}) # create each one of our blocks with the texture manager and a list of textures per face
		self.grass = block_type.Block_type(self.texture_manager, "grass", {"top": "grass", "bottom": "dirt", "sides": "grass_side"})
		self.dirt = block_type.Block_type(self.texture_manager, "dirt", {"all": "dirt"})
		self.stone = block_type.Block_type(self.texture_manager, "stone", {"all": "stone"})
		self.sand = block_type.Block_type(self.texture_manager, "sand", {"all": "sand"})
		self.planks = block_type.Block_type(self.texture_manager, "planks", {"all": "planks"})
		self.log = block_type.Block_type(self.texture_manager, "log", {"top": "log_top", "bottom": "log_top", "sides": "log_side"})

		self.texture_manager.generate_mipmaps() # generate mipmaps for our texture manager's texture


		# creating vertex array object (VAOs) which holds VBOs
		#https://stackoverflow.com/questions/23314787/use-of-vertex-array-objects-and-vertex-buffer-objects

		self.vao = gl.GLuint(0)
		gl.glGenVertexArrays(1, ctypes.byref(self.vao))
		gl.glBindVertexArray(self.vao)

		# creating vertex buffer object(VBOs)
		#https://stackoverflow.com/questions/23314787/use-of-vertex-array-objects-and-vertex-buffer-objects

		self.vertex_position_vbo = gl.GLuint(0)
		gl.glGenBuffers(1, ctypes.byref(self.vertex_position_vbo))
		gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.vertex_position_vbo)
		
		gl.glBufferData(gl.GL_ARRAY_BUFFER,
			ctypes.sizeof(gl.GLfloat * len(self.grass.vertex_positions)),
			(gl.GLfloat * len(self.grass.vertex_positions)) (*self.grass.vertex_positions),
			gl.GL_STATIC_DRAW)
		
		gl.glVertexAttribPointer(0, 3, gl.GL_FLOAT, gl.GL_FALSE, 0, 0)
		gl.glEnableVertexAttribArray(0)
		
		# create tex coord vbo

		self.tex_coord_vbo = gl.GLuint(0)
		gl.glGenBuffers(1, ctypes.byref(self.tex_coord_vbo))
		gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.tex_coord_vbo)

		gl.glBufferData(
			gl.GL_ARRAY_BUFFER,
			ctypes.sizeof(gl.GLfloat * len(self.grass.tex_coords)),
			(gl.GLfloat * len(self.grass.tex_coords)) (*self.grass.tex_coords), # use grass block's texture coordinates positions
			gl.GL_STATIC_DRAW)
		
		gl.glVertexAttribPointer(1, 3, gl.GL_FLOAT, gl.GL_FALSE, 0, 0)
		gl.glEnableVertexAttribArray(1)

		# create index buffer object (IBOs) whichs contains all the indices 
		# https://openglbook.com/chapter-3-index-buffer-objects-and-primitive-types.html

		self.ibo = gl.GLuint(0)
		gl.glGenBuffers(1, self.ibo)
		gl.glBindBuffer(gl.GL_ELEMENT_ARRAY_BUFFER, self.ibo)

		gl.glBufferData(gl.GL_ELEMENT_ARRAY_BUFFER,
			ctypes.sizeof(gl.GLuint * len(self.grass.indices)),
			(gl.GLuint * len(self.grass.indices)) (*self.grass.indices),# use grass block's indices
			gl.GL_STATIC_DRAW)
		
		# creating shader

		self.shader = shader.Shader("vert.glsl", "frag.glsl")
		self.shader_sampler_location = self.shader.find_uniform(b"texture_array_sampler") # find our texture array sampler's uniform
		self.shader.use()

		# pyglet things
		
		pyglet.clock.schedule_interval(self.update, 1.0 / 60) # call update function every 60th of a second
		self.mouse_captured = False

		# camera stuff

		self.camera = camera.Camera(self.shader, self.width, self.height)
	

	def update(self, delta_time):
		if not self.mouse_captured:
			self.camera.input = [0, 0, 0]

		self.camera.update_camera(delta_time)

	def on_draw(self):
		self.camera.update_matrices()
	

		# bind textures

		gl.glActiveTexture(gl.GL_TEXTURE0) # set our active texture unit to the first texture unit
		gl.glBindTexture(gl.GL_TEXTURE_2D_ARRAY, self.texture_manager.texture_array) # bind our texture manager's texture
		gl.glUniform1i(self.shader_sampler_location, 0) # tell our sampler our texture is bound to the first texture unit



		#draw stuff

		gl.glEnable(gl.GL_DEPTH_TEST) # enable depth testing so faces are drawn in the right order
		gl.glClearColor(0.0, 0.0, 0.0, 1.0)
		#gl.glClearColor(1.0, 0.5, 1.0, 1.0) # set clear colour
		self.clear() # clear screen
		
		gl.glDrawElements(gl.GL_TRIANGLES, len(self.grass.indices), gl.GL_UNSIGNED_INT, None) # draw bound buffers to the screen
		

	# input functions

	def on_resize(self, width, height):
		print(f"Resize {width} * {height}") # print out window size, changed from older syntax
		gl.glViewport(0, 0, width, height) # resize the actual OpenGL viewport

		self.camera.width = width
		self.camera.height = height

	def on_mouse_press(self, x, y, button, modifiers):
		self.mouse_captured = not self.mouse_captured
		self.set_exclusive_mouse(self.mouse_captured)

	def on_mouse_motion(self, x, y, delta_x, delta_y):
		if self.mouse_captured:
			sensitivity = 0.004

			self.camera.rotation[0] -= delta_x * sensitivity # this needs to be negative since turning to the left decreases delta_x while increasing the x rotation angle
			self.camera.rotation[1] += delta_y * sensitivity
			
			self.camera.rotation[1] = max(-math.tau / 4, min(math.tau / 4, self.camera.rotation[1])) # clamp the camera's up / down rotation so that you can't snap your neck
	
	def on_key_press(self, key, modifiers):
		if not self.mouse_captured:
			return

		if   key == pyglet.window.key.D: self.camera.input[0] += 1
		elif key == pyglet.window.key.A: self.camera.input[0] -= 1
		elif key == pyglet.window.key.W: self.camera.input[2] += 1
		elif key == pyglet.window.key.S: self.camera.input[2] -= 1

		elif key == pyglet.window.key.SPACE : self.camera.input[1] += 1
		elif key == pyglet.window.key.LSHIFT: self.camera.input[1] -= 1
	
	def on_key_release(self, key, modifiers):
		if not self.mouse_captured:
			return

		if   key == pyglet.window.key.D: self.camera.input[0] -= 1
		elif key == pyglet.window.key.A: self.camera.input[0] += 1
		elif key == pyglet.window.key.W: self.camera.input[2] -= 1
		elif key == pyglet.window.key.S: self.camera.input[2] += 1

		elif key == pyglet.window.key.SPACE : self.camera.input[1] -= 1
		elif key == pyglet.window.key.LSHIFT: self.camera.input[1] += 1

class Game:
	def __init__(self):
		self.config = gl.Config(double_buffer = True, major_version = 3, minor_version = 3, depth_size = 16) # use modern opengl
		self.window = Window(config = self.config, width = 800, height = 600, caption = "Sasta Minecraft", resizable = True, vsync = False) # vsync with pyglet causes problems on some computers, so disable it
	
	def run(self):
		pyglet.app.run() # run our application

if __name__ == "__main__": # only run the game if source file is the one run
	game = Game() # create game object
	game.run()
