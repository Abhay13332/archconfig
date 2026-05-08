// precision mediump float;
// varying vec2 v_texcoord;
// uniform sampler2D tex;

// void main() {
//     vec4 color = texture2D(tex, v_texcoord);

//     // --- MANUAL ADJUSTMENTS ---
//     float saturation = 1.04;  // 1.0 is default. Increase for more vibrance.
//     float contrast = 1.03;    // 1.0 is default. 1.1 makes blacks deeper.
//     float brightness = 1.0;  // 1.0 is default.
//     // -------------------------

//     // Apply Contrast & Brightness
//     color.rgb = ((color.rgb - 0.5) * contrast + 0.5) * brightness;

//     // Apply Saturation (NVIDIA style)
//     float gray = dot(color.rgb, vec3(0.2126, 0.7152, 0.0722));
//     color.rgb = mix(vec3(gray), color.rgb, saturation);

//     gl_FragColor = color;
// }

precision mediump float;
varying vec2 v_texcoord;
uniform sampler2D tex;

// Hyprshade usually provides this, but we use a fallback if not
uniform vec2 screenSize; 

void main() {
    vec2 uv = v_texcoord;
    
    // --- TUNE THESE SETTINGS ---
    // Previous base settings (kept as requested)
    float brightness = 1.0;   // 1.0 is default
    float contrast   = 1.03;  // 1.03 as per your base
    float saturation = 1.04;  // 1.04 as per your base

    // New effects (Currently set to DEFAULT/OFF)
    float gamma      = 1.0;   // 1.0 = No change. Increase (e.g. 1.1) to brighten shadows.
    float sharpen    = 0.0;   // 0.0 = Off. Try 0.1 to 0.3 for crisp text.
    float blueFilter = 0.0;   // 0.0 = Off. Try 0.2 for a warmer "Night Light" feel.
    float vignette   = 0.0;   // 0.0 = Off. Try 0.1 for subtle dark corners.
    
    vec3 colorGain   = vec3(1.0, 1.0, 1.0); // RGB Balance. 1.0 is neutral.
    // ---------------------------

    vec4 color = texture2D(tex, uv);

    // 1. Sharpening (Only runs if sharpen > 0.0)
    if (sharpen > 0.0) {
        vec2 res = (screenSize.x > 0.0) ? screenSize : vec2(1920.0, 1080.0);
        vec2 off = 1.0 / res;
        vec4 neighbors = (
            texture2D(tex, uv + vec2(0, off.y)) +
            texture2D(tex, uv - vec2(0, off.y)) +
            texture2D(tex, uv + vec2(off.x, 0)) +
            texture2D(tex, uv - vec2(off.x, 0))
        );
        color.rgb += (color.rgb - (neighbors.rgb * 0.25)) * sharpen;
    }

    // 2. Apply Contrast, Brightness & Gain
    vec3 outColor = ((color.rgb - 0.5) * contrast + 0.5) * brightness;
    outColor *= colorGain;

    // 3. Apply Gamma
    outColor = pow(max(outColor, 0.0), vec3(1.0 / gamma));

    // 4. Apply Saturation
    float gray = dot(outColor, vec3(0.2126, 0.7152, 0.0722));
    outColor = mix(vec3(gray), outColor, saturation);

    // 5. Apply Blue Light Filter
    outColor.b *= (1.0 - blueFilter);
    outColor.g *= (1.0 - (blueFilter * 0.5));

    // 6. Apply Vignette
    if (vignette > 0.0) {
        float dist = distance(uv, vec2(0.5));
        outColor *= smoothstep(0.8, 0.5 - vignette, dist);
    }

    gl_FragColor = vec4(outColor, color.a);
}

