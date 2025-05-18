import ProjectCard from "@/components/ProjectCard";

const projects = [
  { slug: "tour-centre-ville", title: "Tour Centre-Ville", img: "/images/projet1.webp" },
  { slug: "pont-riviere", title: "Pont de la Rivière", img: "/images/projet2.webp" },
  { slug: "complexe-eco", title: "Complexe Éco-Quartier", img: "/images/projet3.webp" },
  { slug: "condos-montreal-est", title: "Condos Montréal-Est", img: "/images/projet4.webp" },
];

export default function ProjectsSection() {
  return (
    <section id="projets" className="py-20 bg-gray-50 dark:bg-gray-900/40">
      <h2 className="mb-12 text-center text-3xl font-bold">Projets récents</h2>

      <div className="grid gap-8 sm:grid-cols-2 lg:grid-cols-3">
        {projects.map((p) => (
          <ProjectCard key={p.slug} {...p} />
        ))}
      </div>
    </section>
  );
}
