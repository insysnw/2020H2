package lab2.dhcp.options.vendor;

import lab2.dhcp.ConfigurableOptionDescription;

public enum DomainNameOptionDescription implements ConfigurableOptionDescription {
    INSTANCE;

    @Override
    public byte getType() {
        return 15;
    }

    @Override
    public String getName() {
        return "domain-name";
    }

    @Override
    public DomainNameOption produce() {
        return new DomainNameOption();
    }
}
