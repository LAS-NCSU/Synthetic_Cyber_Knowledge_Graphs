from stix2.v21 import (ThreatActor, Identity, AttackPattern, Campaign, IntrusionSet, Relationship, ExternalReference, Bundle)
from stix2validator import validate_file, validate_instance, print_results, validate_string
import json

#test

threat_actor = ThreatActor(
    type="threat-actor",
    spec_version="2.1",
    created="2023-03-01T14:00:00.983Z",
    name="rouge Student",
    description="A disgruntled student angry about a bad test grade",
    threat_actor_types=["insider-disgruntled"],
    roles=["malware-author"],
    goals=["Take the OneUp service offline until grade adjusted"],
    primary_motivation="revenge",
    sophistication="advanced"
)
identity1 = Identity(
    type="identity",
    spec_version="2.1",
    created="2023-03-01T14:00:00.983Z",
    modified="2023-03-01T14:00:00.983Z",
    name="OneUp"
)
attack_pattern1 = AttackPattern(
    type="attack-pattern",
    spec_version="2.1",
    created="2023-03-01T14:00:00.983Z",
    name="DDOS attack"
)
campaign1 = Campaign(
    type="campaign",
    spec_version="2.1",
    created="2023-03-01T14:00:00.983Z",
    name="Operation disguntled student",
    description="A angry student tries to take down the wssu infastructure.",
    aliases=["DSW"],
    objective="shut down OneUp & WebAssign"
)
relationship3 = Relationship(campaign1, 'attributed-to', threat_actor)
relationship1 = Relationship(threat_actor, 'targets', identity1)
relationship2 = Relationship(threat_actor, 'uses', attack_pattern1)

bundle = Bundle(objects=[campaign1,threat_actor, identity1,attack_pattern1, relationship1, relationship2])
#print(bundle.serialize(pretty=True))

with open('bundle.json', 'w') as jsonFile:
    jsonFile.write(bundle.serialize(pretty=True))

#results = validate_string(bundle.serialize(pretty=True))
#print_results(results)
