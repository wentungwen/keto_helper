function generate_sweetness_text(sweet_min, sweet_max, data) {
    if (sweet_max == sweet_min) {
        if (sweet_max == 1) {
        sweet_data = ` ${data.name_cn}的甜度與砂糖差不多`;
        } else {
        sweet_data = ` ${data.name_cn}的甜度是砂糖的 ${sweet_max} 倍`;
        }
    } else {
        sweet_data = ` ${data.name_cn}的甜度是砂糖的 ${sweet_min} - ${sweet_max} 倍`;
    }
    return sweet_data
}


document.addEventListener("DOMContentLoaded", function(){
    fetch("/get-sweetener", {
        method: "GET",
        headers: {
            "Content-Type": "application/json",
        },
        })
        .then((response) => response.json())
        .then((data) => {
            [
                document.getElementById("sweetener-input-select"),
                document.getElementById("sweetener-output-select"),
            ].forEach((item) => {
                item.addEventListener("change", function () {
                    let input_id = document.getElementById("sweetener-input-select").value;
                    let output_id = document.getElementById("sweetener-output-select").value;
                    let input_amount = document.querySelector(".input-sweet input").value;
                    
                
                    input_sweetener = data.data[input_id-1];
                    output_sweetener = data.data[output_id-1];
                    input_text = generate_sweetness_text(input_sweetener.sweetness_min, input_sweetener.sweetness_max, input_sweetener)
                    output_text = generate_sweetness_text(output_sweetener.sweetness_min, output_sweetener.sweetness_max, output_sweetener)
    
                    let output_amount = Math.round(input_amount*(input_sweetener.sweetness_min/output_sweetener.sweetness_min), 2);
    
                    document.getElementById("sweetness-input-value").textContent = input_text;
                    document.getElementById("sweetness-output-value").textContent = output_text;
                    document.querySelector(".output-sweet .result").textContent = `${output_amount}g`;
                });
            });
            
        
        })
        .catch((error) => {
            console.error("Error:", error);
        });
    
})