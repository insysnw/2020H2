package lab2.dhcp.options.dhcp;

import lab2.dhcp.OptionDescription;

public enum BootFileNameOptionDescription implements OptionDescription {
    INSTANCE;

    @Override
    public byte getType() {
        return 67;
    }

    @Override
    public BootFileNameOption produce() {
        return new BootFileNameOption();
    }
}
