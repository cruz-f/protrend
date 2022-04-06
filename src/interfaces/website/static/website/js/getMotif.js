const getMotif = function (imgId, svgId) {
    const imgSelector = document.getElementById(imgId);
    const svgSelector = document.getElementById(svgId);
    const motifSVG = JSON.parse(svgSelector.textContent);
    imgSelector.innerHTML += motifSVG;
}