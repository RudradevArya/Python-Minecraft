#version 330 // specify we are indeed using modern opengl

out vec4 fragment_colour; // output of our shader

in vec3 local_position;  // interpolated vertex position

void main(void) {
	fragment_colour = vec4(local_position / 2.0 + 0.5, 1.0); // set the output colour based on the vertex position
}


//fragment shaders runs on each pixels and computes 
//colours based on the interpolated vaules by vertex 
//shader and outputs to screen

//material to read
//Shaders: https://learnopengl.com/Getting-started/Shaders
//Also shaders: https://antongerdelan.net/opengl/shaders.html
//Ricardo Milos: https://www.urbandictionary.com/define.php?term=Ricardo+Milos
//