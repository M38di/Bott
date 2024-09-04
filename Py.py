import re

# Load the original JSX file
with open('lottieImporter.jsx', 'r') as file:
    jsx_content = file.read()

# Define the code modifications
get_element_check_code = """
function getElementById(id) {
    if(elements[id]) {
        return elements[id].element;
    } else {
        bm_eventDispatcher.log('Element with ID ' + id + ' not found.');
    }
    return null;
}
"""

gradient_handling_code = """
function addGradient(layer, gradientData) {
    if (!gradientData || !layer) return;

    var gradientLayer = layer.property("ADBE Effect Parade").addProperty("ADBE Gradient Ramp");

    if (gradientLayer) {
        gradientLayer.property("ADBE Gradient Ramp-0001").setValue([gradientData.startPoint.x, gradientData.startPoint.y]);
        gradientLayer.property("ADBE Gradient Ramp-0002").setValue([gradientData.endPoint.x, gradientData.endPoint.y]);
        gradientLayer.property("ADBE Gradient Ramp-0003").setValue(gradientData.colors);
    } else {
        bm_eventDispatcher.log('Failed to add gradient to layer: ' + layer.name);
    }
}
"""

# Replace original `getElementById` function with the one that includes logging and null check.
updated_jsx_content = re.sub(
    r'function getElementById[^{]*{[^}]*}', get_element_check_code, jsx_content
)

# Inject the gradient handling code where it would make sense.
# Let's assume we add this function just before the first gradient-related code.

# Adding gradient handling function before the first "gradient" occurrence.
first_gradient_index = re.search(r'gradient', updated_jsx_content, re.IGNORECASE).start()
updated_jsx_content = (
    updated_jsx_content[:first_gradient_index] +
    gradient_handling_code +
    updated_jsx_content[first_gradient_index:]
)

# Save the edited script to a new file
with open('lottieImporter_edited.jsx', 'w') as file:
    file.write(updated_jsx_content)

print("Updated file saved as 'lottieImporter_edited.jsx'")
