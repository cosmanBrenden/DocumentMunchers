// Mock search results used during development.
// Move this file or remove it when wiring a real backend.

export function mockResults(query: string) {
  const base = [
    {
      id: 'r1',
      title: 'The Age of Surveillance Capitalism Chapter 1~5.pdf',
      summary:
        'This article focuses on Surveillance Capitalism, pioneered by Google, extracts human experience as "behavioral surplus" to fabricate prediction products sold for profit, establishing dangerous power asymmetries.',
      relevance: 100,
      lastOpened: '10.3.2025',
      keywords: ['Surveillance Capitalism', 'Behavioral Surplus', 'Extraction Imperative'],
    },
    {
      id: 'r2',
      title: 'Privacy in Context Chapter 1~2.pdf',
      summary:
        'Digital electronic technologies facilitate pervasive "dataveillance" by monitoring and aggregating personal data, enabling omnibus information providers to fundamentally threaten privacy.',
      relevance: 75,
      lastOpened: '10.6.2025',
      keywords: ['Monitoring and Tracking', 'Dataveillance', 'Information Aggregation'],
    },
    {
      id: 'r3',
      title: 'Value Sensitive Design Shaping Technology with Moral Chapter 1~2.pdf',
      summary: 'Exploration of value sensitive design and its implications for designing morally-aware technology and responsible research practices.',
      relevance: 50,
      lastOpened: '9.28.2024',
      keywords: ['Value Sensitive Design', 'Human Values', 'Value Trade-offs'],
    },
    {
      id: 'r4',
      title: 'Do Artifacts Have Politics.pdf',
      summary: 'Classic discussion of how artifacts embed politics and values within design decisions and infrastructures.',
      relevance: 25,
      lastOpened: '10.2.2025',
      keywords: ['Political Qualities', 'Power and Authority', 'Technological Determinism'],
    },
    {
      id: 'r5',
      title: 'A Case for Human Values in Software Engineering.pdf',
      summary: 'Argues for integrating human values explicitly into requirements and engineering practices.',
      relevance: 25,
      lastOpened: '10.3.2025',
      keywords: ['Human Values', 'Requirements Engineering', 'Values Portraits'],
    },
    {
      id: 'r6',
      title: 'Dummy Data.pdf',
      summary: 'Placeholder document used for layout testing.',
      relevance: 10,
      lastOpened: '8.1.2024',
      keywords: ['Test Data', 'Placeholder', 'Layout'],
    },
    {
      id: 'r7',
      title: 'Ethics of AI and Surveillance.pdf',
      summary: 'Survey of ethical issues arising from AI-driven surveillance systems.',
      relevance: 85,
      lastOpened: '11.1.2025',
      keywords: ['AI Ethics', 'Surveillance', 'Privacy'],
    },
    {
      id: 'r8',
      title: 'Data Protection and Law.pdf',
      summary: 'Overview of data protection regimes and their implications for design.',
      relevance: 60,
      lastOpened: '7.20.2025',
      keywords: ['Data Protection', 'Regulation', 'Compliance'],
    },
    {
      id: 'r9',
      title: 'Human-Centered AI Design.pdf',
      summary: 'Design approaches for creating AI systems that center human needs and values.',
      relevance: 70,
      lastOpened: '6.15.2025',
      keywords: ['Human-Centered Design', 'AI Systems', 'Usability'],
    },
  ]

  if (!query) return base
  const q = query.toLowerCase()
  return base
    .map((r) => ({ r, score: r.title.toLowerCase().includes(q) ? 1 : 0 }))
    .sort((a, b) => b.score - a.score)
    .map((x) => x.r)
}
