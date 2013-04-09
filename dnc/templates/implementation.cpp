#include "{{ name }}.h"
#include "RandomNumberGenerator.h"
#include "Utils.h"
#include <cmath>

using namespace std;
using namespace DNest3;

{{ name }}::{{ name }}()
{
}

void {{ name }}::fromPrior()
{
    {%- for param in params %}
    {%- if param.prior %}
    // Prior on {{ param.name }}
    {{ param.prior.strip() }}
    {% endif %}
    {%- endfor %}

    compute_derived();
}

double {{ name }}::perturb() {
    double logH = 0.0;

    compute_derived();
    return logH;
}

void {{ name }}::compute_derived()
{
    {%- for d in derived %}
    {{ d.prior }}
    {%- endfor %}
}

{% for param in params %}
double {{ name }}::perturb_{{ param.name }}()
{
    double logH = 0.;
    {{ param.proposal.strip() }}
    return logH;
}
{% endfor %}

void {{ name }}::print(std::ostream& out) const
{
    {%- for param in params %}
    out<<{{ param.name }}<<' ';
    {%- endfor %}
}

string {{ name }}::description() const
{
    string result = "";
    {%- for param in params %}
    result += "{{ param.name }}";
    result += ", ";
    {%- endfor %}
    return result;
}

double {{ name }}::logLikelihood() const
{
    double logL = 0.;

    return 0.;
}

