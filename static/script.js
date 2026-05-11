async function downloadMedia(mode) {

    const url = document.getElementById("url").value;

    const terminal =
        document.getElementById("terminal");

    if (!url) {

        terminal.innerHTML =
            "Please enter TikTok URL";

        return;
    }

    // LOADING STEPS

    const steps = [

        "Processing request...",

        "Scanning TikTok URL...",

        "Extracting media...",

        "Preparing download...",

        "Finalizing..."

    ];

    let current = 0;

    terminal.innerHTML = steps[0];

    const animation = setInterval(() => {

        current++;

        if (current < steps.length) {

            terminal.innerHTML =
                steps[current];
        }

    }, 800);

    try {

        const response = await fetch("/download", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({

                url: url,
                mode: mode

            })

        });

        const data = await response.json();

        clearInterval(animation);

        // SUCCESS

        if (data.status === "success") {

            terminal.innerHTML =
                "Download ready ✔";

            window.location.href =
                "/file?path=" +
                encodeURIComponent(data.file);

        }

        // ERROR

        else {

            terminal.innerHTML =
                data.message;
        }

    }

    catch (error) {

        clearInterval(animation);

        terminal.innerHTML =
            "Unexpected server error";
    }
}
