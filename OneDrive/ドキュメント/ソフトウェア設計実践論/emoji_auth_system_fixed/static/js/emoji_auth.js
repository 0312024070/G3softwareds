const maxSelectionCount = 3;
const selectedSymbols = [];

const hiddenInput = document.getElementById("selectedSymbols");
const slots = document.querySelectorAll(".selected-slot");
const buttons = document.querySelectorAll(".emoji-button");
const clearButton = document.getElementById("clearButton");
const form = document.getElementById("emojiForm");

function refreshSelectedPanel() {
  slots.forEach((slot, index) => {
    slot.textContent = selectedSymbols[index] || "";
  });
  hiddenInput.value = selectedSymbols.join(",");
}

function clearSelection() {
  selectedSymbols.length = 0;
  buttons.forEach((button) => {
    button.disabled = false;
    button.classList.remove("selected");
  });
  refreshSelectedPanel();
}

buttons.forEach((button) => {
  button.addEventListener("click", () => {
    if (selectedSymbols.length >= maxSelectionCount) {
      return;
    }

    selectedSymbols.push(button.dataset.symbol);
    button.disabled = true;
    button.classList.add("selected");
    refreshSelectedPanel();
  });
});

clearButton.addEventListener("click", clearSelection);

form.addEventListener("submit", (event) => {
  if (selectedSymbols.length !== maxSelectionCount) {
    event.preventDefault();
    alert("3つの絵文字を順番に選択してください。");
  }
});
