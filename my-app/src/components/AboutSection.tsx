import Image from "next/image";

export default function AboutSection() {
  return (
    <section id="apropos" className="py-20">
      <div className="mx-auto grid max-w-5xl gap-12 md:grid-cols-2 md:items-center">
        <Image
          src="/images/equipe.webp"
          alt="Équipe Metanova"
          width={600}
          height={400}
          className="rounded-lg shadow-md"
        />

        <div>
          <h2 className="mb-4 text-3xl font-bold">À propos de Metanova</h2>
          <p className="mb-4">
            Basée à Montréal, Metanova réunit ingénieurs et professionnels passionnés par
            l’innovation. Notre mission : créer des structures durables qui valorisent la
            communauté et le développement urbain.
          </p>
          <p>
            Grâce à une approche multidisciplinaire, nous menons chaque mandat – résidentiel,
            commercial ou institutionnel – avec rigueur et créativité.
          </p>
        </div>
      </div>
    </section>
  );
}
