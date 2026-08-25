import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from technocore.did import Identity, verify  # noqa: E402


def test_did_prefix():
    assert Identity.generate().did.startswith("did:key:z6Mk")


def test_seed_roundtrip():
    me = Identity.generate()
    assert Identity.from_seed_hex(me.seed_hex()).did == me.did


def test_sign_verify():
    me = Identity.generate()
    sig = me.sign("lobby", "123", "gm")
    assert len(sig) == 86
    assert verify(me.did, "lobby", "123", "gm", sig)
    assert not verify(me.did, "lobby", "123", "nope", sig)


def test_known_seed_vector():
    me = Identity.from_seed_hex("06e0e75c3d37f7df0edf76c45547af575b61fe18d1dd8c807b2eabce93228b5b")
    assert me.did == "did:key:z6MkqaWnfiBjUSjxQFcMuVm8FQQgtQKgmLSYTnVgdccri8eV"
