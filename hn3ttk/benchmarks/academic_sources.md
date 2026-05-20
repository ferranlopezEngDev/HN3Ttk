# Academic and Reference Sources for Validation Cases

1. Hardy Cross method

- Classical iterative method for looped pipe network analysis.
- Use as conceptual inspiration for looped validation cases.

2. EPANET

- Rossman, L. A. *EPANET 2 Users Manual*.
- EPANET is a public-domain water distribution network simulator developed by
  the U.S. EPA.
- Use as an external reference for future `.inp` comparison workflows.

3. Water distribution network benchmark literature

- Common benchmark names in the literature include Anytown, Hanoi, New York,
  Balerma, C-Town, D-Town, L-Town and Modena.
- These benchmarks are not implemented here yet unless explicit data is added
  later with a clear provenance and license.

4. Newton-based hydraulic simulation

- Newton and inexact Newton methods are widely used for nonlinear hydraulic
  network equations.
- HN3Ttk uses these ideas as the basis for its custom solver layer and its
  SciPy wrappers.

Do not infer paper-grade numerical validation from these references alone. The
benchmark systems included in HN3Ttk are internal, lightweight and reproducible
teaching and development cases.
