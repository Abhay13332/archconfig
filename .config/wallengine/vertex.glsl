#version 460 core
layout(location=0) in vec2 pos;
layout(location=1) in vec2 texpos;

out vec2 varyvpos;
out vec2 varytexpos;


void main(){
    gl_Position = vec4(pos,0,1.0);
    varyvpos=vec2(1600.0*(texpos.x),900.0*(texpos.y));
    varytexpos=((texpos)+1.0)*0.6;
    
}