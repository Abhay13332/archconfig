precision mediump float;
varying vec2 v_texcoord;
uniform sampler2D tex;

void main() {
    vec4 color = texture2D(tex, v_texcoord);

    // 1. Boost Saturation
    float luminance = dot(color.rgb, vec3(0.2126, 0.7152, 0.0722));
    color.rgb = mix(vec3(luminance), color.rgb, 1.4); // 1.4 is the saturation level

    // 2. Increase Contrast
    color.rgb = (color.rgb - 0.5) * 1.1 + 0.5; // 1.1 increases contrast; keep 0.5 as center

    gl_FragColor = color;
}
