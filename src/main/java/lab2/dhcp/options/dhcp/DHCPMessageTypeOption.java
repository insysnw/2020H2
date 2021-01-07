package lab2.dhcp.options.dhcp;

import lab2.dhcp.Option;
import lab2.dhcp.util.DHCPIllegalFormatException;
import lab2.dhcp.util.Decoder;
import lab2.dhcp.util.Encoder;

public final class DHCPMessageTypeOption implements Option {
    public enum Types {
        NoState, Discover, Offer, Request, Decline, Ack, NotAck, Release, Inform
    }

    private Types type = Types.NoState;

    public Types getType() {
        return type;
    }

    public void setType(Types value) {
        type = value;
    }

    @Override
    public DHCPMessageTypeOptionDescription getDescription() {
        return DHCPMessageTypeOptionDescription.INSTANCE;
    }

    @Override
    public void encode(Encoder encoder) {
        encoder.putByte((byte) type.ordinal());
    }

    @Override
    public void decode(Decoder decoder) {
        byte code = decoder.getByte();
        if (code < 1 || code > 8)
            throw new DHCPIllegalFormatException("illegal DHCP type code: " + code);
        type = Types.values()[code];
    }
}
