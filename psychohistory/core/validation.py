from collections import defaultdict

def validate_observations(obs,as_of):
    errors=[]; warnings=[]; seen=set(); ancestry=defaultdict(int)
    for o in obs:
        if o.available_at>as_of: errors.append(f'future leakage: {o.observation_id}')
        if o.observation_id in seen: errors.append(f'duplicate id: {o.observation_id}')
        seen.add(o.observation_id)
        if not 0<=o.quality<=1: errors.append(f'invalid quality: {o.observation_id}')
        if o.revision_type not in {'none','scheduled_revision','maturation','methodological_revision','correction'}: warnings.append(f'unknown revision type: {o.observation_id}')
        for a in o.ancestry: ancestry[a]+=1
    dependent={k:v for k,v in ancestry.items() if v>1}
    return {'valid':not errors,'errors':errors,'warnings':warnings,'shared_ancestry':dependent,'informational_breadth_upper_bound':len(obs)-sum(v-1 for v in dependent.values())}
