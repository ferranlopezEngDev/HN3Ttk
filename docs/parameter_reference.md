# Parameter Reference

This page summarizes the public parameter dictionaries accepted by the main
HN3Ttk models.

HN3Ttk now exports editor-friendly `TypedDict` definitions so VS Code and
similar tools can suggest supported keys inside `parameters={...}` blocks.

Example:

```python
from hn3ttk.connections import PipeFixedPowerLaw, PipeFixedPowerLawParameters
from hn3ttk.nodes import DemandNode, DemandNodeParameters

demand_parameters: DemandNodeParameters = {
    "elevation": 0.0,
    "initial_head": 5.0,
    "demand": 0.1,
}

pipe_parameters: PipeFixedPowerLawParameters = {
    "k": 100.0,
    "n": 2.0,
}

demand = DemandNode(parameters=demand_parameters)
pipe = PipeFixedPowerLaw(parameters=pipe_parameters)
```

Notes:

- The `TypedDict` keys are editor hints and static typing helpers.
- Runtime validation still happens in each model `validate()` method.
- Many keys are optional because defaults are filled automatically at runtime.

## Nodes

### `ConfigurableNodeParameters`

| Key | Meaning | Required | Default |
|---|---|---|---|
| `elevation` | Node elevation `z` [m] | no | `0.0` |
| `fixed_head` | Whether the head is prescribed | no | `False` |
| `head` | Prescribed hydraulic head [m] | no | `elevation` |
| `initial_head` | Initial guess for unknown head [m] | no | `elevation` |
| `external_flow` | Signed external flow [m3/s] | no | `0.0` |
| `scale_head_with_alpha` | Scale fixed head during continuation | no | `False` |
| `scale_external_flow_with_alpha` | Scale external flow during continuation | no | `True` |

### `JunctionNodeParameters`

| Key | Meaning | Required | Default |
|---|---|---|---|
| `elevation` | Node elevation `z` [m] | no | `0.0` |
| `initial_head` | Initial unknown-head guess [m] | no | `elevation` |
| `external_flow` | Signed external flow [m3/s] | no | `0.0` |
| `scale_external_flow_with_alpha` | Scale external flow during continuation | no | `True` |

### `DemandNodeParameters`

| Key | Meaning | Required | Default |
|---|---|---|---|
| `elevation` | Node elevation `z` [m] | no | `0.0` |
| `initial_head` | Initial unknown-head guess [m] | no | `elevation` |
| `demand` | Demand magnitude [m3/s] | yes | none |
| `scale_demand_with_alpha` | Scale demand during continuation | no | `True` |

### `InjectionNodeParameters`

| Key | Meaning | Required | Default |
|---|---|---|---|
| `elevation` | Node elevation `z` [m] | no | `0.0` |
| `initial_head` | Initial unknown-head guess [m] | no | `elevation` |
| `injection` | Injection magnitude [m3/s] | yes | none |
| `scale_injection_with_alpha` | Scale injection during continuation | no | `True` |

### `FixedHeadNodeParameters` and `ReservoirNodeParameters`

| Key | Meaning | Required | Default |
|---|---|---|---|
| `elevation` | Node elevation `z` [m] | no | `0.0` |
| `head` | Prescribed hydraulic head [m] | yes | none |
| `scale_head_with_alpha` | Scale head from elevation to final head | no | `False` |

## Connections

### Shared optional connection keys

These keys are accepted by all connection models:

| Key | Meaning | Default |
|---|---|---|
| `jacobian_derivative` | Jacobian strategy: `normal`, `tendency`, `inverse_head_loss`, `finite_difference` | `normal` |
| `jacobian_derivative_step` | Relative finite-difference step for Jacobian fallback | `1.0e-6` |
| `jacobian_derivative_absolute_step` | Absolute finite-difference step for Jacobian fallback | `1.0e-10` |

### `PipeFixedPowerLawParameters`

| Key | Meaning | Required | Default |
|---|---|---|---|
| `k` | Power-law coefficient | yes | none |
| `n` | Power-law exponent | yes | none |
| `head_tolerance` | Zero-head threshold for inversion | no | `1.0e-12` |

### `PipeDarcyParameters`

| Key | Meaning | Required | Default |
|---|---|---|---|
| `length` | Pipe length [m] | yes | none |
| `diameter` | Internal diameter [m] | yes | none |
| `roughness` | Absolute roughness [m] | yes | none |
| `kinematic_viscosity` | Fluid kinematic viscosity [m2/s] | no | `1.0e-6` |
| `gravity` | Gravity [m/s2] | no | `9.81` |
| `laminar_reynolds` | Laminar threshold | no | `2000.0` |
| `turbulent_reynolds` | Turbulent threshold | no | `4000.0` |
| `head_tolerance` | Zero-head threshold for inversion | no | `1.0e-12` |
| `inverse_relative_tolerance` | Relative tolerance for inverse solve | no | `1.0e-10` |
| `inverse_max_iterations` | Maximum inverse iterations | no | `100` |
| `derivative_relative_step` | Relative step for model derivative | no | `1.0e-6` |
| `derivative_absolute_step` | Absolute step for model derivative | no | `1.0e-10` |

### `PipeLocalPowerLawParameters`

| Key | Meaning | Required | Default |
|---|---|---|---|
| `length` | Pipe length [m] | yes | none |
| `diameter` | Internal diameter [m] | yes | none |
| `roughness` | Absolute roughness [m] | yes | none |
| `kinematic_viscosity` | Fluid kinematic viscosity [m2/s] | no | `1.0e-6` |
| `gravity` | Gravity [m/s2] | no | `9.81` |
| `laminar_reynolds` | Laminar threshold | no | `2000.0` |
| `turbulent_reynolds` | Turbulent threshold | no | `4000.0` |
| `relative_band` | Local fitting band | no | `0.05` |
| `minimum_flow_rate` | Minimum magnitude for local fit | no | `1.0e-8` |
| `head_tolerance` | Zero-head threshold for inversion | no | `1.0e-12` |
| `inverse_relative_tolerance` | Relative tolerance for inverse solve | no | `1.0e-10` |
| `inverse_max_iterations` | Maximum inverse iterations | no | `100` |
| `derivative_relative_step` | Relative step for model derivative | no | `1.0e-6` |
| `derivative_absolute_step` | Absolute step for model derivative | no | `1.0e-10` |

### `LinearInterpolationConnectionParameters`

| Key | Meaning | Required | Default |
|---|---|---|---|
| `flow_rates` | Sampled flow-rate values | yes | none |
| `head_losses` | Sampled head-variation values | yes | none |
| `extrapolate` | Allow extrapolation outside sampled range | no | `True` |

### `PolynomialRegressionConnectionParameters`

| Key | Meaning | Required | Default |
|---|---|---|---|
| `flow_rates` | Sampled flow-rate values | yes | none |
| `head_losses` | Sampled head-variation values | yes | none |
| `degree` | Regression polynomial degree | no | `1` |
| `extrapolate` | Allow extrapolation outside sampled range | no | `True` |
| `inverse_scan_points` | Scan points for inverse bracketing | no | `200` |
| `inverse_max_iterations` | Maximum inverse iterations | no | `100` |
| `head_tolerance` | Head tolerance for inverse solve | no | `1.0e-12` |
| `flow_tolerance` | Flow tolerance for inverse solve | no | `1.0e-12` |

### `SplineInterpolationConnectionParameters`

| Key | Meaning | Required | Default |
|---|---|---|---|
| `flow_rates` | Sampled flow-rate values | yes | none |
| `head_losses` | Sampled head-variation values | yes | none |
| `method` | `pchip` or `cubic_spline` | no | `pchip` |
| `extrapolate` | Allow extrapolation outside sampled range | no | `True` |

### `CustomFactorPolynomialConnectionParameters`

| Key | Meaning | Required | Default |
|---|---|---|---|
| `coefficients` | Positive polynomial coefficients | yes | none |
| `exponents` | Positive exponents | yes | none |
| `head_tolerance` | Zero-head threshold for inversion | no | `1.0e-12` |
| `inverse_relative_tolerance` | Relative tolerance for inverse solve | no | `1.0e-10` |
| `inverse_max_iterations` | Maximum inverse iterations | no | `100` |
| `minimum_flow_rate` | Minimum magnitude used near zero flow | no | `1.0e-12` |

## Solver option aliases

HN3Ttk also exports literal type aliases for common string options:

- `JacobianDerivativeMode`
- `ScipyRootMethod`
- `ScipyLeastSquaresMethod`
- `SplineInterpolationMethod`

Example:

```python
from hn3ttk.solvers import JacobianDerivativeMode, ScipyRootMethod

derivative_mode: JacobianDerivativeMode = "finite_difference"
root_method: ScipyRootMethod = "hybr"
```
