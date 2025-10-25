/**
 * Orval config - async-safe, TS-friendly
 */
import 'dotenv/config';
import { defineConfig } from "orval";
import fs from "fs";
import path from "path";
import axios from "axios";

const pascal = (s: string) =>
  s.replace(/(^\w|[-_]\w)/g, (m) => m.replace(/[-_]/, "").toUpperCase());

const features = [
  { name: "auth", swaggerUrl: process.env.NEXT_PUBLIC_AUTH_BASE_URL },
  // add more...
];

const ensureFeatureStructure = (feature: string) => {
  const base = path.resolve(`src/features/${feature}`);
  ["helpers", "interfaces", "hooks", "views"].forEach((dir) => {
    const full = path.join(base, dir);
    if (!fs.existsSync(full)) fs.mkdirSync(full, { recursive: true });
  });
  const indexFile = path.join(base, "index.ts");
  if (!fs.existsSync(indexFile)) {
    fs.writeFileSync(
      indexFile,
      `// ${feature} feature entry\nexport * from './helpers/api';\nexport * from './hooks';\n`
    );
  }
};

const generateFeatureFiles = async (feature: string, swaggerUrl: string) => {
  if (!swaggerUrl) {
    console.warn(`⚠️ Missing swaggerUrl for feature "${feature}"`);
    return;
  }

  const base = path.resolve(`src/features/${feature}`);
  const controllerFile = path.join(base, "helpers", "controller.ts");
  const hooksDir = path.join(base, "hooks");

  const swagger = (await axios.get(swaggerUrl)).data;
  let controllerCode = `import { queryOptions, useQuery, useMutation } from '@tanstack/react-query';\nimport * as api from './api';\n\n`;

  for (const [pathKey, methods] of Object.entries(swagger.paths)) {
    for (const [method, details] of Object.entries(methods as any)) {
      const op = details as { operationId?: string };
      const rawName = op.operationId || `${method}_${pathKey.replace(/[\\/{}]/g, "_")}`;
      const funcName = pascal(rawName);
      const hookName = `use${funcName}`;
      const queryParams = `${funcName}QueryParams`;
      const responseType = `${funcName}Response`;

      if (method.toLowerCase() === "get") {
        controllerCode += `export const ${rawName}Controller = (
  params: ${queryParams},
  setData: (data: ${responseType}) => void
) =>
  queryOptions({
    queryKey: ['${rawName}', params],
    queryFn: async () => {
      const res = await api.${rawName}(params);
      setData(res);
      return res;
    },
    retry: false,
    refetchOnMount: false,
    enabled: !!params,
  });\n\n`;

        const hookCode = `import { useQuery } from '@tanstack/react-query';\nimport { ${rawName}Controller } from '../helpers/controller';\nimport type { ${queryParams}, ${responseType} } from '../helpers/api';\n\nexport const ${hookName} = (params: ${queryParams}, setData: (data: ${responseType}) => void) => {\n  return useQuery(${rawName}Controller(params, setData));\n};\n`;
        fs.writeFileSync(path.join(hooksDir, `${hookName}.ts`), hookCode);
      } else {
        controllerCode += `export const ${rawName}Mutation = () => useMutation<${responseType}, Error, ${queryParams}>({
  mutationFn: api.${rawName},
});\n\n`;

        const hookCode = `import { ${rawName}Mutation } from '../helpers/controller';\nimport type { ${queryParams}, ${responseType} } from '../helpers/api';\n\nexport const ${hookName} = () => {\n  return ${rawName}Mutation();\n};\n`;
        fs.writeFileSync(path.join(hooksDir, `${hookName}.ts`), hookCode);
      }
    }
  }

  fs.writeFileSync(controllerFile, controllerCode);
};

export default defineConfig(async () => {
  // pre-generate folders & controllers/hooks
  for (const f of features) {
    ensureFeatureStructure(f.name);
    try {
      await generateFeatureFiles(f.name, f.swaggerUrl ?? "");
    } catch (err: any) {
      console.error(`❌ Error generating feature "${f.name}":`, err.message);
    }
  }

  // Return Orval config WITHOUT 'override.operations' to avoid TS mismatch
  return Object.fromEntries(
    features.map((f) => {
      if (!f.swaggerUrl) {
        throw new Error(`Missing swaggerUrl for feature "${f.name}"`);
      }

      return [
        f.name,
        {
          input: { target: f.swaggerUrl! },
          output: {
            mode: "tags-split",
            target: `src/features/${f.name}/helpers/api.ts`,
            schemas: `src/features/${f.name}/interfaces`,
            client: "axios",
            prettier: true,
            override: {
              mutator: {
                path: "src/libs/axiosInstance.ts",
                name: "axiosInstance",
              },
              // <-- removed 'operations' here to satisfy TypeScript
            },
          },
        },
      ];
    })
  );
});
