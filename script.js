document.getElementById('salaryForm').addEventListener('submit', async function (e) {
    e.preventDefault();


    const experienceInput = document.getElementById('experience');
    const roleSelect = document.getElementById('role');
    const educationSelect = document.getElementById('education');
    const locationSelect = document.getElementById('location');
    const companyTypeSelect = document.getElementById('company_type');

    const resultOverlay = document.getElementById('resultOverlay');
    const salaryAmount = document.getElementById('salaryAmount');
    const submitBtn = this.querySelector('button[type="submit"]');

    
    const requestData = {
        "Experience": parseFloat(experienceInput.value), 
        "Role": roleSelect.value,
        "Education": educationSelect.value,
        "Location": locationSelect.value,
        "Company_Type": companyTypeSelect.value
    };

    const originalBtnText = submitBtn.innerText;
    submitBtn.innerText = "Calculating...";
    submitBtn.disabled = true;
    submitBtn.classList.add('opacity-75', 'cursor-not-allowed');

    try {
        const response = await fetch('http://127.0.0.1:8000/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(requestData)
        });

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        const data = await response.json();
        const finalSalary = data.salary || data.prediction || 0;
        const formattedSalary = new Intl.NumberFormat('en-IN', {
            style: 'currency',
            currency: 'INR',
            maximumFractionDigits: 0
        }).format(finalSalary);

        salaryAmount.innerText = formattedSalary;
        resultOverlay.classList.remove('hidden');

    } catch (error) {
        // console.error('Error:', error);
        salaryAmount.innerText = "Error";
        alert("Failed to get prediction.");
    } finally {
        submitBtn.innerText = originalBtnText;
        submitBtn.disabled = false;
        submitBtn.classList.remove('opacity-75', 'cursor-not-allowed');
    }
});