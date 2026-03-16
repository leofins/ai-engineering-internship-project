import { useState } from "react";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import {
  Sparkles,
  Brain,
  Database,
  Zap,
  Shield,
  BarChart3,
  GitBranch,
  Cloud,
  Code,
  ArrowRight,
} from "lucide-react";

const features = [
  { icon: Brain, title: "Integracao com LLM", description: "Suporte a OpenAI, Google Gemini e modelos locais com streaming de respostas em tempo real." },
  { icon: Database, title: "RAG Avancado", description: "Sistema de Retrieval-Augmented Generation com ChromaDB para busca semantica inteligente." },
  { icon: Zap, title: "Upload de Documentos", description: "Suporte a PDF, TXT e Markdown com processamento automatico e indexacao vetorial." },
  { icon: Shield, title: "Seguranca", description: "Validacao de entrada, CORS configuravel e sanitizacao de uploads." },
  { icon: BarChart3, title: "Monitoramento", description: "Health checks, logs estruturados e estatisticas de colecao em tempo real." },
  { icon: GitBranch, title: "CI/CD Pipeline", description: "Automacao com GitHub Actions incluindo testes, build e security scanning." },
];

const techStack = [
  { category: "Backend", items: ["FastAPI", "Python 3.11", "ChromaDB", "Uvicorn"] },
  { category: "Frontend", items: ["React 19", "TypeScript", "Tailwind CSS 4", "Streamdown"] },
  { category: "DevOps", items: ["Docker", "docker-compose", "GitHub Actions", "Trivy"] },
  { category: "Testing", items: ["Pytest", "Vitest", "Coverage", "Mypy"] },
];

const endpoints = [
  { method: "POST", path: "/api/chat", description: "Chat com contexto RAG" },
  { method: "POST", path: "/api/chat/stream", description: "Chat com streaming" },
  { method: "POST", path: "/api/upload", description: "Upload de documentos" },
  { method: "POST", path: "/api/search", description: "Busca semantica" },
  { method: "GET", path: "/api/collection/stats", description: "Estatisticas" },
  { method: "DELETE", path: "/api/collection/clear", description: "Limpar colecao" },
];

export default function ProjectShowcase() {
  const [activeTab, setActiveTab] = useState<"features" | "tech" | "api">("features");

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900">
      <section className="relative overflow-hidden px-4 py-20 sm:px-6 lg:px-8">
        <div className="mx-auto max-w-6xl text-center">
          <div className="flex items-center justify-center mb-6">
            <Sparkles className="w-16 h-16 text-blue-400 animate-pulse" />
          </div>
          <h1 className="text-5xl sm:text-6xl font-bold text-white mb-6">RAG System</h1>
          <p className="text-xl text-slate-300 mb-8 max-w-2xl mx-auto">
            Sistema elegante de Retrieval-Augmented Generation com integracao de modelos de linguagem avancados.
          </p>
          <div className="flex gap-4 justify-center flex-wrap">
            <Button size="lg" className="bg-blue-600 hover:bg-blue-700">
              <Sparkles className="w-4 h-4 mr-2" /> Explorar Dados
            </Button>
            <Button size="lg" variant="outline" className="border-slate-600 hover:bg-slate-700">
              <Code className="w-4 h-4 mr-2" /> Ver Codigo
            </Button>
          </div>
        </div>
      </section>

      <section className="px-4 py-16 sm:px-6 lg:px-8 border-y border-slate-700">
        <div className="mx-auto max-w-6xl">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
            {[
              { label: "Endpoints API", value: "6+" },
              { label: "Formatos Suportados", value: "3" },
              { label: "Provedores LLM", value: "3+" },
              { label: "Cobertura de Testes", value: "85%+" },
            ].map((stat, i) => (
              <div key={i} className="text-center">
                <div className="text-4xl font-bold text-blue-400 mb-2">{stat.value}</div>
                <div className="text-slate-400">{stat.label}</div>
              </div>
            ))}
          </div>
        </div>
      </section>

      <section className="px-4 py-20 sm:px-6 lg:px-8">
        <div className="mx-auto max-w-6xl">
          <h2 className="text-4xl font-bold text-white mb-12 text-center">Funcionalidades Principais</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {features.map((feature, i) => {
              const Icon = feature.icon;
              return (
                <Card key={i} className="bg-slate-800 border-slate-700 p-6 hover:border-blue-500 transition-colors">
                  <Icon className="w-12 h-12 text-blue-400 mb-4" />
                  <h3 className="text-xl font-semibold text-white mb-2">{feature.title}</h3>
                  <p className="text-slate-400">{feature.description}</p>
                </Card>
              );
            })}
          </div>
        </div>
      </section>

      <section className="px-4 py-20 sm:px-6 lg:px-8 bg-slate-800/50">
        <div className="mx-auto max-w-6xl">
          <h2 className="text-4xl font-bold text-white mb-12 text-center">Stack Tecnologico</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            {techStack.map((stack, i) => (
              <Card key={i} className="bg-slate-800 border-slate-700 p-6">
                <h3 className="text-lg font-semibold text-blue-400 mb-4">{stack.category}</h3>
                <ul className="space-y-2">
                  {stack.items.map((item, j) => (
                    <li key={j} className="text-slate-300 text-sm">{item}</li>
                  ))}
                </ul>
              </Card>
            ))}
          </div>
        </div>
      </section>

      <section className="px-4 py-20 sm:px-6 lg:px-8">
        <div className="mx-auto max-w-6xl">
          <h2 className="text-4xl font-bold text-white mb-4 text-center">API Endpoints</h2>
          <div className="mb-6 flex gap-4">
            {(["features", "tech", "api"] as const).map((tab) => (
              <Button
                key={tab}
                variant={activeTab === tab ? "default" : "outline"}
                onClick={() => setActiveTab(tab)}
                className={activeTab === tab ? "bg-blue-600" : "border-slate-600"}
              >
                {tab === "features" ? "Funcionalidades" : tab === "tech" ? "Tecnologias" : "API"}
              </Button>
            ))}
          </div>
          <div className="space-y-4">
            {endpoints.map((ep, i) => (
              <Card key={i} className="bg-slate-800 border-slate-700 p-4 flex items-center gap-4">
                <span className={`px-2 py-1 rounded text-xs font-bold ${
                  ep.method === "GET" ? "bg-green-600 text-white" :
                  ep.method === "POST" ? "bg-blue-600 text-white" :
                  "bg-red-600 text-white"
                }`}>{ep.method}</span>
                <code className="text-slate-300 font-mono">{ep.path}</code>
                <span className="text-slate-400 text-sm">{ep.description}</span>
              </Card>
            ))}
          </div>
        </div>
      </section>

      <section className="px-4 py-20 sm:px-6 lg:px-8 bg-gradient-to-r from-blue-600 to-blue-700">
        <div className="mx-auto max-w-4xl text-center">
          <h2 className="text-4xl font-bold text-white mb-6">Pronto para Comecar?</h2>
          <p className="text-xl text-blue-100 mb-8">
            Acesse a interface de chat para fazer upload de documentos e explorar o poder do RAG com LLM.
          </p>
          <Button size="lg" className="bg-white text-blue-600 hover:bg-slate-100">
            Ir para Chat <ArrowRight className="w-4 h-4 ml-2" />
          </Button>
        </div>
      </section>

      <footer className="px-4 py-8 sm:px-6 lg:px-8 border-t border-slate-700 bg-slate-900">
        <div className="mx-auto max-w-6xl text-center text-slate-400">
          <p>Desenvolvido como parte do programa de estagio em Engenharia de IA</p>
          <p className="mt-2 text-sm">© 2024 RAG System. Todos os direitos reservados.</p>
        </div>
      </footer>
    </div>
  );
}
