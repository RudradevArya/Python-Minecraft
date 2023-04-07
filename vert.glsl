#version 330 // specify we are indeed using modern opengl

layout(location = 0) in vec3 vertex_position; // vertex position attribute

out vec3 local_position; // interpolated vertex position

uniform mat4 matrix;

void main(void) {
	local_position = vertex_position;
	gl_Position = matrix * vec4(vertex_position, 1.0);// multiply matrix by vertex_position vector
}



//vertex shaders are little programs that run on GPus 
//for each index of the scene and they output vertex position 
//and other data based on the atributes from that index

//material to read
//Shaders: https://learnopengl.com/Getting-started/Shaders
//Also shaders: https://antongerdelan.net/opengl/shaders.html
//Ricardo Milos: https://www.urbandictionary.com/define.php?term=Ricardo+Milos
//