import json
import os
import unitypack
import sys
from argparse import ArgumentParser

#python generate_sounds.py --outdir="D:\Game\Hearthstone\HearthstoneJSON\sounds" --cards-json-path="D:\Game\Hearthstone\HearthstoneJSON\cards.json" "D:\Game\Hearthstone\Data\Win" one-dir
def generate_json(folder, cards_list):
    sounds_json = {}
    stinger_json = {}
    manifest_file_list = ['asset_manifest.unity3d','asset_manifest_zhcn.unity3d']
    for file in manifest_file_list:
        manifest_file = os.path.join(folder, file)
        with open(manifest_file, 'rb') as f:
            bundle = unitypack.load(f)
            for asset in bundle.assets:
                for obj in asset.objects.values():
                    if obj.type == 'ScriptableAssetCatalog':
                        d = obj.read()
                        flag = False
                        for a in d['m_assets']:
                            splited_path = a['Path'].split('/')
                            if flag:
                                if 'stinger' in splited_path[-1].lower():
                                    if last_id not in stinger_json:
                                        stinger_json[last_id] = [splited_path[-1][:-4]]
                                    else:
                                        stinger_json[last_id].append(splited_path[-1][:-4])
                                flag = False
                                continue
                            if(a['Path'][-3:] == 'wav'):
                                for temp in splited_path:
                                    if temp in cards_list:
                                        last_id = temp
                                        if temp not in sounds_json:
                                            sounds_json[temp] = [splited_path[-1][:-4]]
                                        else:
                                            sounds_json[temp].append(splited_path[-1][:-4])
                                        break
                            if splited_path[-1][-6:] == 'prefab' and 'music' in splited_path[-1].lower() and 'stinger' in splited_path[-1].lower():
                                flag = True

    return sounds_json, stinger_json

def output_sounds(folder, outdir, sounds_json, one_dir):
    reverted_map = {}
    for card_id, sounds_list in sounds_json.items():
        for sound in sounds_list:
            reverted_map[sound] = card_id
    for filename in sorted(os.listdir(folder)):
        if filename[-7:] == 'unity3d' and ('zhcn' in filename or 'global' in filename):
            print('Reading ' + filename)
            with open(os.path.join(folder,filename), "rb") as f:
                bundle = unitypack.load(f)
                for asset in bundle.assets:
                    print("Parsing %r" % (asset.name))
                    for obj in asset.objects.values():
                        if obj.type == 'AudioClip':
                            sounds_dict = unitypack.utils.extract_audioclip_samples(obj.read())
                            for sound_name, sound in sounds_dict.items():
                                if(sound_name[:-4] in reverted_map):
                                    card_id = reverted_map[sound_name[:-4]]
                                    if one_dir:
                                        path = os.path.join(outdir,sound_name)
                                    else:
                                        if not os.path.exists(os.path.join(outdir,card_id)):
                                            os.makedirs(os.path.join(outdir,card_id))
                                        path = os.path.join(outdir,card_id,sound_name)
                                    with open(path,'wb') as file:
                                        file.write(sound.tobytes())

                                    

def main():
    p = ArgumentParser()
    p.add_argument("--outdir", nargs="?", default="")
    p.add_argument("--json-only", action="store_true", help="Only write JSON cardinfo")
    p.add_argument("--cards-json-path", nargs="?",default="cards.json")
    p.add_argument("--one-dir", action="store_true", help="output in one dir")
    p.add_argument("folder")
    args = p.parse_args(sys.argv[1:])
    with open(args.cards_json_path, encoding='utf-8') as file:
        cards_json = json.load(file)
    cards_list = []
    for card in cards_json:
        cards_list.append(card['id'])
    
    sounds_json, stinger_json = generate_json(args.folder, cards_list)
    with open("sounds.json", 'w', encoding='utf-8') as file:
        json.dump(sounds_json, file)
    with open("stingers.json", 'w', encoding='utf-8') as file:
        json.dump(stinger_json, file)
    if not args.json_only:
        output_sounds(args.folder, args.outdir, sounds_json, args.one_dir)

if __name__ == "__main__":
    main()