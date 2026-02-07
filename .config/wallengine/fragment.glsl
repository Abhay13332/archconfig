#version 460 core
precision mediump float;
in vec2 varyvpos;
in vec2 varytexpos;
out vec4 FragColor;

uniform float radius;
uniform float pointerX;
uniform float pointerY;
uniform sampler2D txt1;
uniform sampler2D txt2;
uniform vec4 txt_dimension;

void main(){
    float x=(float(varyvpos.x));

    int calc=(varyvpos.x-pointerX*1.6+270.0)*(varyvpos.x-pointerX*1.6+270.0)+(varyvpos.y+pointerY*1.58+160.0)*(varyvpos.y+pointerY*1.58+160.0)<radius?1:0;

    // FragColor = vec4(abs(sin(radius+varyvpos.y)),abs(cos(radius+x)),0.7,0);
    float min_txt1=min(txt_dimension.x/1920.0,txt_dimension.y/1080.0);
    float min_txt2=min(txt_dimension.z/1920.0,txt_dimension.w/1080.0); 
    FragColor = mix(texture(txt1,min_txt1*vec2(varytexpos.x*1920.0/txt_dimension.x,varytexpos.y*1080.0/txt_dimension.y)),texture(txt2,min_txt2*vec2(varytexpos.x*1920.0/txt_dimension.z,varytexpos.y*1080.0/txt_dimension.w)),float(calc));
}