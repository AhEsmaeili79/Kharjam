import 'dotenv/config';
import { defineConfig } from "orval";
import fs from "fs";
import path from "path";
import axios from "axios";



const mergeInterfaces = () => {
    const featuresDir = path.resolve("src/features");
    const outputDir = path.resolve("src/interfaces");
    const outputFile = path.join(outputDir, "interfaces.ts");
  
    if (!fs.existsSync(outputDir)) fs.mkdirSync(outputDir, { recursive: true });
  
    let merged = `// Auto-generated combined interfaces\n`;
  
    // Loop through all features
    const features = fs.readdirSync(featuresDir);
    for (const feature of features) {
      const interfacesDir = path.join(featuresDir, feature, "interfaces");
      if (fs.existsSync(interfacesDir)) {
        const files = fs.readdirSync(interfacesDir).filter(f => f.endsWith(".ts"));
        for (const file of files) {
          const filePath = path.join(interfacesDir, file);
          const content = fs.readFileSync(filePath, "utf8");
          merged += `\n// ===== ${feature}/${file} =====\n` + content + "\n";
        }
      }
    }
  
    fs.writeFileSync(outputFile, merged);
    console.log(`✅ Merged all interfaces into: ${outputFile}`);
  };
  
  // Run after Orval completes
  (async () => {
    const orig = (await import("../orval.config")).default;
    if (typeof orig === "function") {
      await orig();
    }
    mergeInterfaces();
  })();
  
  