document.addEventListener('DOMContentLoaded', () => {

    /**
     * Menangani pengiriman form untuk perhitungan numerik.
     * @param {string} formId - ID dari form HTML.
     * @param {string} url - URL endpoint API di backend.
     * @param {function} getPayload - Fungsi untuk membuat payload JSON dari data form.
     */
    async function handleFormSubmit(formId, url, getPayload) {
        const form = document.getElementById(formId);
        if (!form) return;

        form.addEventListener('submit', async (event) => {
            event.preventDefault();
            const resultDiv = document.getElementById('result');
            resultDiv.style.display = 'block';
            resultDiv.className = '';
            resultDiv.innerHTML = '<p>Menghitung...</p>';

            try {
                const payload = getPayload(form);
                const response = await fetch(url, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(payload),
                });

                const data = await response.json();

                if (response.ok) {
                    displayResult(formId, data, resultDiv);
                } else {
                    resultDiv.className = 'error';
                    resultDiv.innerHTML = `<h3>Error</h3><p>${data.error}</p>`;
                }
            } catch (error) {
                resultDiv.className = 'error';
                resultDiv.innerHTML = `<h3>Error</h3><p>Tidak dapat menghubungi server: ${error.message}</p>`;
            }
        });
    }

    /**
     * Menampilkan hasil perhitungan di div hasil.
     * @param {string} formId - ID form untuk menentukan format output.
     * @param {object} data - Data hasil dari backend.
     * @param {HTMLElement} resultDiv - Elemen div untuk menampilkan hasil.
     */
    function displayResult(formId, data, resultDiv) {
        let content = '<h3>Hasil Perhitungan</h3>';
        switch (formId) {
            case 'maclaurin-form':
                content += `<p>Bentuk Deret:</p><p class="code-block">${data.series_polynomial}</p>`;
                content += `<p>Hasil Aproksimasi: <strong>${data.result.toFixed(8)}</strong></p>`;
                break;
            case 'gaussseidel-form':
                const solutionText = data.solution.map((val, i) => `x${i + 1} = ${val.toFixed(6)}`).join('<br>');
                content += `<p>Solusi ditemukan dalam <strong>${data.iterations}</strong> iterasi:</p>`;
                content += `<p class="code-block">${solutionText}</p>`;
                break;
            default: // Untuk metode pencarian akar
                content += `<p>Akar yang ditemukan: <strong>${data.root.toFixed(8)}</strong></p>`;
                content += `<p>Ditemukan dalam <strong>${data.iterations}</strong> iterasi.</p>`;
        }
        resultDiv.innerHTML = content;
    }

    /**
     * Menangani logika untuk tombol analisis AI.
     */
    function handleAiAnalysis() {
        const analyzeButton = document.getElementById('analyze-button');
        const caseStudyInput = document.getElementById('case-study-input');
        const resultDiv = document.getElementById('result');
        const form = document.querySelector('form');

        if (!analyzeButton || !caseStudyInput || !form) return;

        const methodType = form.id.replace('-form', '')
            .replace('newtonraphson', 'newton_raphson')
            .replace('regulafalsi', 'regula_falsi')
            .replace('gaussseidel', 'gauss_seidel');

        analyzeButton.addEventListener('click', async () => {
            const caseText = caseStudyInput.value;
            if (!caseText.trim()) {
                alert('Silakan masukkan teks studi kasus terlebih dahulu.');
                return;
            }

            resultDiv.style.display = 'block';
            resultDiv.className = '';
            resultDiv.innerHTML = '<p>🤖 Menganalisis dengan AI, mohon tunggu...</p>';
            analyzeButton.disabled = true;
            analyzeButton.textContent = 'Menganalisis...';

            try {
                const response = await fetch('/analyze-case', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ text: caseText, method: methodType }),
                });

                const data = await response.json();

                if (response.ok) {
                    const params = JSON.parse(data.parameters);
                    for (const key in params) {
                        const inputElement = document.getElementById(key);
                        if (inputElement) {
                            inputElement.value = params[key];
                        }
                    }
                    resultDiv.innerHTML = '<p>✅ Analisis selesai. Form telah diisi otomatis.</p>';
                } else {
                    resultDiv.className = 'error';
                    resultDiv.innerHTML = `<h3>Error AI</h3><p>${data.error}</p>`;
                }
            } catch (error) {
                resultDiv.className = 'error';
                resultDiv.innerHTML = `<h3>Error AI</h3><p>Gagal memproses permintaan: ${error.message}</p>`;
            } finally {
                analyzeButton.disabled = false;
                analyzeButton.textContent = 'Analisis dengan AI';
            }
        });
    }

    // Mengaktifkan semua handler untuk form yang ada
    handleFormSubmit('bisection-form', '/calculate/bisection', form => ({
        function: form.querySelector('#function').value,
        a: form.querySelector('#a').value,
        b: form.querySelector('#b').value,
        tolerance: form.querySelector('#tolerance').value,
    }));
    handleFormSubmit('regulafalsi-form', '/calculate/regula-falsi', form => ({
        function: form.querySelector('#function').value,
        a: form.querySelector('#a').value,
        b: form.querySelector('#b').value,
        tolerance: form.querySelector('#tolerance').value,
    }));
    handleFormSubmit('newtonraphson-form', '/calculate/newton-raphson', form => ({
        function: form.querySelector('#function').value,
        x0: form.querySelector('#x0').value,
        tolerance: form.querySelector('#tolerance').value,
    }));
    handleFormSubmit('secant-form', '/calculate/secant', form => ({
        function: form.querySelector('#function').value,
        x0: form.querySelector('#x0').value,
        x1: form.querySelector('#x1').value,
        tolerance: form.querySelector('#tolerance').value,
    }));
    handleFormSubmit('maclaurin-form', '/calculate/maclaurin', form => ({
        function: form.querySelector('#function').value,
        x_value: form.querySelector('#x_value').value,
        terms: form.querySelector('#terms').value,
    }));
    handleFormSubmit('gaussseidel-form', '/calculate/gauss-seidel', form => ({
        matrix_a: form.querySelector('#matrix_a').value,
        vector_b: form.querySelector('#vector_b').value,
        tolerance: form.querySelector('#tolerance').value,
        max_iter: form.querySelector('#max_iter').value,
    }));

    // Mengaktifkan handler untuk fitur AI
    handleAiAnalysis();
});