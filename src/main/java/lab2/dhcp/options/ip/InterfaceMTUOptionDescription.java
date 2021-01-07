package lab2.dhcp.options.ip;

import lab2.dhcp.ConfigurableOptionDescription;

public enum InterfaceMTUOptionDescription implements ConfigurableOptionDescription {
    INSTANCE;

    @Override
    public byte getType() {
        return 26;
    }

    @Override
    public String getName() {
        return "interface-mtu";
    }

    @Override
    public InterfaceMTUOption produce() {
        return new InterfaceMTUOption();
    }
}
