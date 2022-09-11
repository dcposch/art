import { select } from "d3-selection";
import treePath from "./tree";

console.log("Hello world");

const svg = select("svg").attr("fill", "none").attr("stroke", "#282");
const disgust = svg.nodes()[0] as SVGSVGElement;
const w = disgust.width.animVal.value; // 50 years gulag for the API designer
const h = disgust.height.animVal.value;
svg.append("path").attr("d", treePath(w, h));

document.querySelector("a#dl").addEventListener("mousedown", saveSvg);

function saveSvg(event: MouseEvent) {
  const svgEl = document.querySelector("svg");
  svgEl.setAttribute("xmlns", "http://www.w3.org/2000/svg");
  const svgData = svgEl.outerHTML;
  const preface = '<?xml version="1.0" standalone="no"?>\r\n';
  const type = "image/svg+xml;charset=utf-8";
  const svgBlob = new Blob([preface, svgData], { type });
  const svgUrl = URL.createObjectURL(svgBlob);
  const downloadLink = event.currentTarget as HTMLAnchorElement;
  downloadLink.href = svgUrl;
  const date = new Date().toISOString().substring(0, 16).replace(/[T:]/g, "-");
  downloadLink.download = `out-${date}.svg`;
}
