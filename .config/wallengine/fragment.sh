#version 320 es
precision mediump float;
in vec2 varyvpos;
in vec2 varytexpos;
out vec4 FragColor;

uniform float radius;
uniform float pointerX;
uniform float pointerY;
uniform sampler2D txt1;
uniform sampler2D txt2;

void main(){
    float x=(float(varyvpos.x));

    int calc=(varyvpos.x-pointerX*1.6+270.0)*(varyvpos.x-pointerX*1.6+270.0)+(varyvpos.y+pointerY*1.58+160.0)*(varyvpos.y+pointerY*1.58+160.0)<radius?1:0;

    // FragColor = vec4(abs(sin(radius+varyvpos.y)),abs(cos(radius+x)),0.7,0); 
    FragColor = mix(texture(txt1,varytexpos),texture(txt2,varytexpos),float(calc));
}