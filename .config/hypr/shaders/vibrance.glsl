precision mediump float;
varying vec2 v_texcoord;
uniform sampler2D tex;

void main() {
    vec4 color = texture2D(tex, v_texcoord);
    float avg = (color.r + color.g + color.b) / 3.0;
    float mx = max(color.r, max(color.g, color.b));
    float amt = (mx - avg) * 0.75; // Adjust 0.75 higher for more vibrance
    gl_FragColor = vec4(color.rgb + amt * (color.rgb - mx), color.a);
}
