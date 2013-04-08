class Normal:
    def __init__(self, name, mean, sd):
        self.name = name
        self.mean = mean
        self.sd = sd

    def fromPrior(self):
        parts = []
        parts.append(self.name)
        parts.append(" = ")
        parts.append(str(self.mean))
        parts.append(" + ")
        parts.append(str(self.sd))
        parts.append("*randn();")
        return ''.join(parts)

    def perturb(self):
        lines = []
        template = 'double _#name = (#name - #mean)/#sd;'
        lines.append(template)
        template = 'logH -= -0.5*pow(_#name, 2);'
        lines.append(template)
        template = '_#name += #sd*pow(10., 1.5 - 6.*randomU())*randn();'
        lines.append(template)
        template = 'logH += -0.5*pow(_#name, 2);'
        lines.append(template)
        template = '#name = #mean + #sd*_#name;'
        lines.append(template)
        result = '\n'.join(lines)
        result = result.replace('#name', self.name)
        result = result.replace('#mean', str(self.mean))
        result = result.replace('#sd', str(self.sd))
        return result

    def logProb(self):
        parts = []
        parts.append("logL += -0.5*log(2.*M_PI) - log(#sd) ")
        parts.append("- 0.5*pow((#name - #mean)/#sd, 2);")
        result = ''.join(parts)
        result = result.replace('#name', self.name)
        result = result.replace('#mean', str(self.mean))
        result = result.replace('#sd', str(self.sd))
        return result


    def __str__(self):
        return self.name


class Uniform:
    def __init__(self, name, a, b):
        self.name = name
        self.a = a
        self.b = b

    def fromPrior(self):
        parts = []
        parts.append(self.name)
        parts.append(" = ")
        parts.append(str(self.a))
        parts.append(" + (")
        parts.append(str(self.b))
        parts.append(" - ")
        parts.append(str(self.a))
        parts.append(")*randomU();")
        return ''.join(parts)

    def perturb(self):
        parts = []
        parts.append("#name += (")
        parts.append(str(self.b))
        parts.append(" - ")
        parts.append(str(self.a))
        parts.append(")*pow(10., 1.5 - 6.*randomU())*randn();\n")
        parts.append("#name = mod(#name - #a, #b - #a);")
        result = ''.join(parts)
        result = result.replace('#name', self.name)
        result = result.replace('#a', str(self.a))
        result = result.replace('#b', str(self.b))
        return result

    def logProb(self):
        parts = []
        parts.append("if(#name < #a || #name > #b)\n\tlogL = -1E300;\n")
        parts.append("else\n\t")
        parts.append("logL += -log(#b - #a);\n")
        result = ''.join(parts)
        result = result.replace('#name', self.name)
        result = result.replace('#a', str(self.a))
        result = result.replace('#b', str(self.b))
        return result

    def __str__(self):
        return self.name


if __name__ == '__main__':
    theta = Normal("theta", "a", "b")
    print(theta.fromPrior())
    print()
    print(theta.perturb())
    print()
