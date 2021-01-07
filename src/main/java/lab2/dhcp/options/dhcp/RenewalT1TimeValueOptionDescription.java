package lab2.dhcp.options.dhcp;

import lab2.dhcp.OptionDescription;

public enum RenewalT1TimeValueOptionDescription implements OptionDescription {
    INSTANCE;

    @Override
    public byte getType() {
        return 58;
    }

    @Override
    public RenewalT1TimeValueOption produce() {
        return new RenewalT1TimeValueOption();
    }
}
