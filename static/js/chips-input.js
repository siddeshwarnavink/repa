customElements.define("chips-input", class extends HTMLElement {
	constructor() {
		super();
		this._chips = [];
		this._buttonListeners = [];
		this.attachShadow({ mode: "open" });

		this.shadowRoot.innerHTML = `
		<style>
		    .form-chips-input {
                 display: flex;
                 border: 1px solid #ccc;
				 width: 350px;
				 padding: 10px 12px;
				 font-size: 1.2rem;
                 flex-wrap: wrap;
			 }

			.chips-input {
				border: none;
				outline: none;
				font-size: 1.2rem; width: 100px;
			}

			#chips-list {
                display: flex;
                flex-wrap: wrap;
			}

            #chips-list .chip-item {
                display: flex;
                align-items: center;
                border-radius: 20px;
                background-color: #ccc;
                padding: 5px 10px;
                font-size: 12px;
                margin-top: 1px;
                margin-bottom: 1px;
                margin-right: 5px;
            }

            #chips-list .chip-item button {
                border: 0;
                border-radius: 50%;
                background-color: #ccc;
                padding: 2px;
                cursor: pointer;
            }
		</style>
		<div class="form-chips-input">
            <div id="chips-list"></div>
			<input id="chip-input" class="chips-input" />
		</div>
		`;
	}

    connectedCallback() {
		this.hiddenInput = document.createElement("input");
        this.hiddenInput.type = "hidden";
        const name = this.getAttribute("name");
        if (name) {
            this.hiddenInput.name = name;
        }
        this.updateHiddenInput();
        this.appendChild(this.hiddenInput);

		this.renderChips();
        this.shadowRoot
			.getElementById("chip-input")
			.addEventListener("keydown", this.handleKeyDown.bind(this));
    }

	removeChipButtonListeners() {
		this._buttonListeners.forEach(({ button, listener }) => {
			button.removeEventListener("click", listener);
		});
		this._buttonListeners = [];
	}

	renderChips() {
		const chipsList = this.shadowRoot.getElementById("chips-list");
		chipsList.innerHTML = "";
		this.removeChipButtonListeners();

		this._chips.forEach((chip, index) => {
			const div = document.createElement("div");
			div.innerHTML = `
			<div class="chip-item">
				${chip}
				<button>x</button>
			</div>
			`;
			chipsList.appendChild(div);

			const button = div.querySelector("button");
			const listener = () => this.removeChip(index);
			button.addEventListener("click", listener);

			this._buttonListeners.push({ button, listener });
		});

		this.updateHiddenInput();
	}

	removeChip(index) {
		this._chips.splice(index, 1);
		this.renderChips();
	}

	// #chip-input onkeydown
    handleKeyDown(event) {
		const inputBox = this.shadowRoot.getElementById("chip-input");
		switch (event.key) {
		case "Enter":
			this._chips.push(inputBox.value);
			inputBox.value = "";
			this.renderChips();
			break;
		case "Backspace":
			if (inputBox.value === "") {
				this._chips.pop();
				this.renderChips();
			}
			break;
		}
    }

	updateHiddenInput() {
		if (this.hiddenInput) {
			this.hiddenInput.value = this._chips.join(",");
		}
	}

	disconnectedCallback() {
        this.shadowRoot
			.getElementById("chip-input")
			.removeEventListener("keydown", this.handleKeyDown.bind(this));
		this.removeChipButtonListeners();

		if (this.hiddenInput && this.hiddenInput.parentNode) {
            this.hiddenInput.parentNode.removeChild(this.hiddenInput);
        }
    }
});
