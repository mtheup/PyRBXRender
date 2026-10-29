                      
                       
"""Roblox character and mesh renderer."""
import argparse, base64, io, json, math, os, re, struct, sys, zlib
import xml.etree.ElementTree as ET
import numpy as np
from PIL import Image

                                                                              
                                                                      
                                                                              
BRICK = json.loads(r'''{"2":["Grey",161,165,162],"3":["Light yellow",249,233,153],"5":["Brick yellow",215,197,153],"9":["Light reddish violet",232,186,199],"11":["Pastel Blue",128,187,219],"12":["Light orange brown",203,132,66],"18":["Nougat",204,142,104],"21":["Bright red",196,40,27],"22":["Med. reddish violet",196,112,160],"23":["Bright blue",13,105,171],"24":["Bright yellow",245,205,47],"25":["Earth orange",98,71,50],"26":["Black",27,42,52],"27":["Dark grey",109,110,108],"28":["Dark green",40,127,70],"29":["Medium green",161,196,139],"36":["Lig. Yellowich orange",243,207,155],"37":["Bright green",75,151,74],"38":["Dark orange",160,95,52],"39":["Light bluish violet",193,202,222],"40":["Transparent",236,236,236],"41":["Tr. Red",205,84,75],"42":["Tr. Lg blue",193,223,240],"43":["Tr. Blue",123,182,232],"44":["Tr. Yellow",247,241,141],"45":["Light blue",180,210,227],"47":["Tr. Flu. Reddish orange",217,133,108],"48":["Tr. Green",132,182,141],"49":["Tr. Flu. Green",248,241,132],"50":["Phosph. White",236,232,222],"100":["Light red",238,196,182],"101":["Medium red",218,134,121],"102":["Medium blue",110,153,201],"103":["Light grey",199,193,183],"104":["Bright violet",107,50,123],"105":["Br. yellowish orange",226,155,63],"106":["Bright orange",218,133,64],"108":["Earth yellow",104,92,67],"110":["Bright bluish violet",67,84,147],"111":["Tr. Brown",191,183,177],"112":["Medium bluish violet",104,116,172],"113":["Tr. Medi. reddish violet",228,173,200],"115":["Med. yellowish green",199,210,60],"116":["Med. bluish green",85,165,175],"118":["Light bluish green",183,215,213],"119":["Br. yellowish green",164,189,70],"120":["Lig. yellowish green",217,228,167],"121":["Med. yellowish orange",231,172,88],"123":["Br. reddish orange",211,111,76],"124":["Bright reddish violet",146,57,120],"125":["Light orange",234,184,145],"126":["Tr. Bright bluish violet",165,165,203],"127":["Gold",220,188,129],"128":["Dark nougat",174,122,89],"131":["Silver",156,163,168],"133":["Neon orange",213,115,61],"134":["Neon green",216,221,86],"135":["Sand blue",116,134,156],"136":["Sand violet",135,124,144],"137":["Medium orange",224,152,100],"138":["Sand yellow",149,138,115],"140":["Earth blue",32,58,86],"141":["Earth green",39,70,44],"143":["Tr. Flu. Blue",207,226,247],"145":["Sand blue metallic",121,136,161],"146":["Sand violet metallic",149,142,163],"147":["Sand yellow metallic",147,135,103],"148":["Dark grey metallic",87,88,87],"149":["Black metallic",22,29,50],"150":["Light grey metallic",171,173,172],"151":["Sand green",120,144,129],"153":["Sand red",149,121,118],"154":["Dark red",123,46,47],"157":["Tr. Flu. Yellow",255,246,123],"158":["Tr. Flu. Red",225,164,194],"168":["Gun metallic",117,108,98],"176":["Red flip/flop",151,105,91],"178":["Yellow flip/flop",180,132,85],"179":["Silver flip/flop",137,135,136],"180":["Curry",215,169,75],"190":["Fire Yellow",249,214,46],"191":["Flame yellowish orange",232,171,45],"192":["Reddish brown",105,64,39],"193":["Flame reddish orange",207,96,36],"194":["Medium stone grey",163,162,164],"195":["Royal blue",70,103,164],"196":["Dark Royal blue",35,71,139],"198":["Bright reddish lilac",142,66,133],"199":["Dark stone grey",99,95,97],"200":["Lemon metalic",130,138,93],"208":["Light stone grey",229,228,222],"209":["Dark Curry",176,142,68],"210":["Faded green",112,149,120],"211":["Turquoise",121,181,181],"212":["Light Royal blue",159,195,233],"213":["Medium Royal blue",108,129,183],"216":["Rust",143,76,42],"217":["Brown",124,92,69],"218":["Reddish lilac",150,112,159],"219":["Lilac",107,98,155],"220":["Light lilac",167,169,206],"221":["Bright purple",205,98,152],"222":["Light purple",228,173,200],"223":["Light pink",220,144,149],"224":["Light brick yellow",240,213,160],"225":["Warm yellowish orange",235,184,127],"226":["Cool yellow",253,234,140],"232":["Dove blue",125,187,221],"268":["Medium lilac",52,43,117]}''')
BRICK = {int(k): v for k, v in BRICK.items()}
BRICK.setdefault(1, ["White", 242, 243, 243])                                    


def brick_rgb(num):
    e = BRICK.get(int(num))
    if e is None:
        pass
        return np.array([0.64, 0.64, 0.64], np.float32)
    return np.array(e[1:4], np.float32) / 255.0


                                                                              
                                                              
                                                                              
_B64 = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz._"


def _decode_name(n):
    out = ""
    for ch in n:
        c = ord(ch)
        if 0x3800 <= c < 0x4800:
            c -= 0x3800
            out += _B64[c & 0x3F] + _B64[(c >> 6) & 0x3F]
        elif 0x4800 <= c < 0x4840:
            out += _B64[c - 0x4800]
        elif c == 0x4840:
            out += "$"
        else:
            out += ch
    return out


class OLE:
    def __init__(self, path):
        d = self.d = open(path, "rb").read()
        assert d[:8] == bytes.fromhex("D0CF11E0A1B11AE1"), "nao e um arquivo OLE/MSI"
        self.ssz = 1 << struct.unpack_from("<H", d, 30)[0]
        self.mssz = 1 << struct.unpack_from("<H", d, 32)[0]
        nfat, dirstart, _, cutoff, mf_start, n_mf, difat_start, n_difat = struct.unpack_from("<IIIIIIII", d, 44)
        self.cutoff = cutoff
        difat = list(struct.unpack_from("<109I", d, 76))
        s, per = difat_start, self.ssz // 4 - 1
        for _ in range(n_difat):
            vals = struct.unpack_from("<%dI" % (per + 1), d, (s + 1) * self.ssz)
            difat += vals[:per]
            s = vals[per]
        self.fat = []
        for s in [x for x in difat if x < 0xFFFFFFFA][:nfat]:
            self.fat += struct.unpack_from("<%dI" % (self.ssz // 4), d, (s + 1) * self.ssz)
        dd = self.chain(dirstart)
        self.entries = []
        for i in range(len(dd) // 128):
            e = dd[i * 128:(i + 1) * 128]
            nl = struct.unpack_from("<H", e, 64)[0]
            left, right, child = struct.unpack_from("<III", e, 68)
            self.entries.append(dict(
                name=e[:max(nl - 2, 0)].decode("utf-16le"), type=e[66], left=left, right=right,
                child=child, start=struct.unpack_from("<I", e, 116)[0],
                size=struct.unpack_from("<Q", e, 120)[0] & 0xFFFFFFFF))
        root = self.entries[0]
        self.mini = self.chain(root["start"])[:root["size"]] if root["size"] else b""
        self.minifat = []
        if n_mf:
            mf = self.chain(mf_start)
            self.minifat = list(struct.unpack("<%dI" % (len(mf) // 4), mf))

    def chain(self, s):
        out, seen = bytearray(), set()
        while s < 0xFFFFFFFA and s not in seen:
            seen.add(s)
            o = (s + 1) * self.ssz
            out += self.d[o:o + self.ssz]
            s = self.fat[s]
        return bytes(out)

    def minichain(self, s):
        out, seen = bytearray(), set()
        while s < 0xFFFFFFFA and s not in seen:
            seen.add(s)
            out += self.mini[s * self.mssz:(s + 1) * self.mssz]
            s = self.minifat[s]
        return bytes(out)

    def stream(self, e):
        if e["size"] < self.cutoff:
            return self.minichain(e["start"])[:e["size"]]
        return self.chain(e["start"])[:e["size"]]

    def streams(self):
        res = []

        def rec(i):
            if i == 0xFFFFFFFF:
                return
            e = self.entries[i]
            rec(e["left"])
            res.append(e)
            rec(e["right"])
        rec(self.entries[0]["child"])
        return [e for e in res if e["type"] == 2]


class MSI:
    def __init__(self, path):
        self.ole = OLE(path)
        self.streams = {_decode_name(e["name"]): e for e in self.ole.streams()}
        self._strings()
        cols = self._raw_table("_Columns", [("Table", "s"), ("Number", "i"), ("Name", "s"), ("Type", "i")])
        self.schema = {}
        for r in cols:
            self.schema.setdefault(r["Table"], []).append((r["Number"] & 0x7FFF, r["Name"], r["Type"] & 0xFFFF))
        for t in self.schema:
            self.schema[t].sort()

    def raw(self, name):
        return self.ole.stream(self.streams[name])

    def _strings(self):
        pool, data = self.raw("$_StringPool"), self.raw("$_StringData")
        cp = struct.unpack_from("<I", pool, 0)[0]
        self.sidx = 3 if cp & 0x80000000 else 2
        enc = "cp%d" % (cp & 0x7FFFFFFF) if cp & 0x7FFFFFFF else "cp1252"
        self.strs, i, pos = [""], 4, 0
        while i < len(pool):
            ln, rc = struct.unpack_from("<HH", pool, i)
            i += 4
            if ln == 0 and rc != 0:
                lo = struct.unpack_from("<H", pool, i)[0]
                ln, rc = (rc << 16) | lo, struct.unpack_from("<H", pool, i + 2)[0]
                i += 4
            self.strs.append(data[pos:pos + ln].decode(enc, errors="replace"))
            pos += ln

    def _s(self, i):
        return self.strs[i] if 0 < i < len(self.strs) else ""

    def _raw_table(self, name, cols):
        key = "$" + name
        if key not in self.streams:
            return []
        data = self.raw(key)
        sz = {"s": self.sidx, "i": 2}
        rowsize = sum(sz[t] for _, t in cols)
        n = len(data) // rowsize
        rows, pos = [dict() for _ in range(n)], 0
        for cn, t in cols:
            for r in range(n):
                v = int.from_bytes(data[pos:pos + sz[t]], "little")
                pos += sz[t]
                rows[r][cn] = self._s(v) if t == "s" else v
        return rows

    def table(self, name):
        key = "$" + name
        if key not in self.streams or name not in self.schema:
            return None
        cols = self.schema[name]

        def w(t):
            return self.sidx if t & 0x0800 else (4 if (t & 0xFF) == 4 else 2)
        data = self.raw(key)
        rowsize = sum(w(t) for _, _, t in cols)
        n = len(data) // rowsize
        rows, pos = [[None] * len(cols) for _ in range(n)], 0
        for ci, (_, _, t) in enumerate(cols):
            ww = w(t)
            for r in range(n):
                v = int.from_bytes(data[pos:pos + ww], "little")
                pos += ww
                if t & 0x0800:
                    v = self._s(v)
                else:
                    v = (v - (0x8000 if ww == 2 else 0x80000000)) if v else None
                rows[r][ci] = v
        return [c[1] for c in cols], rows


def cab_files(cab):

    _, _, _, _, coff_files, _, _, _, n_folders, n_files, flags, _, _ = struct.unpack_from("<4sIIIIIBBHHHHH", cab, 0)
    off = 36
    if flags & 4:
        cb_res = struct.unpack_from("<H", cab, 36)[0]
        off += 4 + cb_res
    folders = []
    for _ in range(n_folders):
        folders.append(struct.unpack_from("<IHH", cab, off))
        off += 8
    p, files = coff_files, []
    for _ in range(n_files):
        cb, uoff, ifold = struct.unpack_from("<IIH", cab, p)
        p += 16
        e = cab.index(b"\0", p)
        files.append((cab[p:e].decode("latin1"), cb, uoff, ifold))
        p = e + 1
    fdata = {}
    for fi, (start, nblk, comp) in enumerate(folders):
        assert comp & 0xF == 1, "so CAB MSZIP e suportado"
        q, out, hist = start, bytearray(), b""
        for _ in range(nblk):
            _, cb, cu = struct.unpack_from("<IHH", cab, q)
            q += 8
            blk = cab[q:q + cb]
            q += cb
            dobj = zlib.decompressobj(-15, zdict=hist) if hist else zlib.decompressobj(-15)
            data = dobj.decompress(blk[2:]) + dobj.flush()
            out += data
            hist = data
        fdata[fi] = bytes(out)
    return {n: fdata[fi][uo:uo + cb] for n, cb, uo, fi in files}


def cmd_setup(a):
    msi = MSI(a.msi)
    fc, files = msi.table("File")
    cc, comps = msi.table("Component")
    dc, dirs = msi.table("Directory")
    mc, media = msi.table("Media")
    fi, ci, di, mi = ({c: i for i, c in enumerate(t)} for t in (fc, cc, dc, mc))
    dmap = {r[di["Directory"]]: (r[di["Directory_Parent"]], r[di["DefaultDir"]]) for r in dirs}
    comp_dir = {r[ci["Component"]]: r[ci["Directory_"]] for r in comps}

    def dpath(d):
        parts, seen = [], set()
        while d and d in dmap and d not in seen:
            seen.add(d)
            parent, dd = dmap[d]
            name = (dd or "").split(":")[-1].split("|")[-1]
            if name not in ("", ".", "SourceDir") and d != "TARGETDIR":
                parts.append(name)
            d = parent
        return "/".join(reversed(parts))

    cab = {}
    for r in media:
        cabname = (r[mi["Cabinet"]] or "").lstrip("#")
        if cabname and cabname in msi.streams:
            cab.update(cab_files(msi.raw(cabname)))
    keep = {".png", ".jpg", ".jpeg", ".rbxm", ".mesh", ".lua", ".txt", ".tga", ".bmp"}
    n = 0
    for r in files:
        key = r[fi["File"]]
        fname = r[fi["FileName"]].split("|")[-1]
        ext = os.path.splitext(fname)[1].lower()
        if not a.all and ext not in keep:
            continue
        if key not in cab:
            continue
        path = os.path.join(a.assets, dpath(comp_dir.get(r[fi["Component_"]], "")), fname)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        open(path, "wb").write(cab[key])
        n += 1
    print(f"Extracted {n} files to {a.assets}/")


                                                                              
        
                                                                              
_ASSET_INDEX = {}


def asset_index(root):
    if root not in _ASSET_INDEX:
        idx = {}
        for dp, _, fs in os.walk(root):
            for f in fs:
                idx.setdefault(f.lower(), os.path.join(dp, f))
        _ASSET_INDEX[root] = idx
    return _ASSET_INDEX[root]


def find_asset(root, ref):

    if os.path.isfile(ref):
        return ref
    base = re.split(r"[\\/]", ref)[-1].lower()
    return asset_index(root).get(base)


def load_rgba(src):
    im = Image.open(src).convert("RGBA")
    a = np.asarray(im, np.float32) / 255.0
    a[..., :3] *= a[..., 3:4]                                                      
    return a


                                                                              
                               
                                                                              
class Scene:
    def __init__(self):
        self.P, self.N, self.A, self.M, self.mats = [], [], [], [], []

    def material(self, **kw):
        kw.setdefault("color", np.array([0.64, 0.64, 0.64], np.float32))
        kw.setdefault("surf", None)                                  
        kw.setdefault("decal", None)                             
        kw.setdefault("wrap", False)
        self.mats.append(kw)
        return len(self.mats) - 1

    def add(self, P, N, A, m):

        self.P.append(np.asarray(P, np.float32))
        self.N.append(np.asarray(N, np.float32))
        self.A.append(np.asarray(A, np.float32))
        self.M.append(np.full(len(P), m, np.int32))

    def done(self):
        self.P, self.N, self.A, self.M = (np.concatenate(x) for x in (self.P, self.N, self.A, self.M))
        return self


                                                                                                    
FACES = {
    0: ((1, 0, 0), (0, 0, -1), (0, 1, 0)),
    1: ((0, 1, 0), (-1, 0, 0), (0, 0, 1)),
    2: ((0, 0, 1), (1, 0, 0), (0, 1, 0)),
    3: ((-1, 0, 0), (0, 0, 1), (0, 1, 0)),
    4: ((0, -1, 0), (1, 0, 0), (0, 0, 1)),
    5: ((0, 0, -1), (-1, 0, 0), (0, 1, 0)),
}
SURF_PROP = ["RightSurface", "TopSurface", "BackSurface", "LeftSurface", "BottomSurface", "FrontSurface"]


class Tiles:


    def __init__(self, path, stud_variant=0):
        g = np.asarray(Image.open(path).convert("L"), np.float32) / 255.0
        col, row = stud_variant % 2, (stud_variant // 2) % 4
        raw = {
            3: g[row * 32:(row + 1) * 32, col * 32:(col + 1) * 32],                 
            4: g[128 + row * 32:128 + (row + 1) * 32, col * 32:(col + 1) * 32],          
            5: g[256:320, 0:64],                                                         
            1: g[384:448, 0:64],                                                    
        }
        self.t = {k: (v / v.mean())[..., None].astype(np.float32) for k, v in raw.items()}


def add_box(sc, R, pos, size, mats):
    size = np.asarray(size, np.float32)
    for nid, (n, r, u) in FACES.items():
        n, r, u = (np.array(v, np.float32) for v in (n, r, u))
        en, er, eu = (float(np.abs(v) @ size) for v in (n, r, u))
        c = n * en / 2
        corners = [c - r * er / 2 - u * eu / 2, c + r * er / 2 - u * eu / 2,
                   c + r * er / 2 + u * eu / 2, c - r * er / 2 + u * eu / 2]
        A = []
        for p in corners:
            su, sv = float(p @ r) + er / 2, eu / 2 - float(p @ u)
            A.append([su, sv, su / er, sv / eu, 1.0])
        W = [R @ p + pos for p in corners]
        Nw = np.tile(R @ n, (4, 1))
        m = mats[nid]
        sc.add([[W[0], W[1], W[2]], [W[0], W[2], W[3]]], [Nw[:3], Nw[:3]], [[A[0], A[1], A[2]], [A[0], A[2], A[3]]], m)


def add_head(sc, R, pos, scale, m, segs=64, bevel=0.16):

    sx, sy, sz = scale
    rad_x, rad_z, h = 0.5 * sx, 0.5 * sz, 1.0 * sy
    b = bevel * (sx + sy + sz) / 3
    prof = [(0.0, h / 2, 0.0, 1.0)]
    for k in range(0, 7):
        a = math.radians(k * 15)
        prof.append(((1 - b / (0.5 * sx)) * 0.5 * sx + b * math.sin(a), h / 2 - b + b * math.cos(a), math.sin(a), math.cos(a)))
    for k in range(6, 13):
        a = math.radians(k * 15)
        prof.append(((1 - b / (0.5 * sx)) * 0.5 * sx + b * math.sin(a), -h / 2 + b + b * math.cos(a), math.sin(a), math.cos(a)))
    prof.append((0.0, -h / 2, 0.0, -1.0))
    th = np.linspace(0, 2 * math.pi, segs + 1)

    def vert(i, j):
        rr, y, nr, ny = prof[i]
        x, z = rr * math.cos(th[j]) * (rad_x / (0.5 * sx)), rr * math.sin(th[j]) * (rad_z / (0.5 * sz))
        nx, nz = nr * math.cos(th[j]), nr * math.sin(th[j])
        loc = np.array([x, y, z], np.float32)
        nl = np.array([nx / (rad_x / (0.5 * sx)), ny, nz / (rad_z / (0.5 * sz))], np.float32)
        nl /= np.linalg.norm(nl) + 1e-9
                                                                                  
        a = [0, 0, 0.5 - x / (2 * rad_x), 0.5 - y / h, -z / rad_z]
        return R @ loc + pos, R @ nl, a
    P, N, A = [], [], []
    for i in range(len(prof) - 1):
        for j in range(segs):
            v = [vert(i, j), vert(i + 1, j), vert(i + 1, j + 1), vert(i, j + 1)]
            for tri in ((0, 1, 2), (0, 2, 3)):
                P.append([v[k][0] for k in tri])
                N.append([v[k][1] for k in tri])
                A.append([v[k][2] for k in tri])
    sc.add(P, N, A, m)


def load_mesh_v1(path):

    txt = open(path, "r", errors="replace").read()
    nums = [[float(x) for x in g.split(",")] for g in re.findall(r"\[([^\]]+)\]", txt)]
    v = np.array(nums, np.float32).reshape(-1, 3, 3)                                      
    return v[:, 0], v[:, 1], v[:, 2][:, :2]


def add_filemesh(sc, R, pos, path, scale, m, mesh_scale=0.5, flip_v=True):
    p, n, uv = load_mesh_v1(path)
    p = p * mesh_scale * np.asarray(scale, np.float32)
    nn = n / (np.linalg.norm(n, axis=1, keepdims=True) + 1e-9)
    v = 1 - uv[:, 1] if flip_v else uv[:, 1]
    A = np.stack([np.zeros(len(p)), np.zeros(len(p)), uv[:, 0], v, np.ones(len(p))], 1)
    T = len(p) // 3
    sc.add((p @ R.T + pos).reshape(T, 3, 3), (nn @ R.T).reshape(T, 3, 3), A.reshape(T, 3, 5), m)


                                                                              
                                      
                                                                              
def _props(item):
    d = {}
    pr = item.find("Properties")
    if pr is None:
        return d
    for p in pr:
        n = p.get("name")
        if p.tag == "CoordinateFrame":
            d[n] = {c.tag: float(c.text) for c in p}
        elif p.tag in ("Vector3", "Color3"):
            d[n] = [float(c.text) for c in p]
        elif p.tag == "Content":
            kid = list(p)
            d[n] = ("bin", "".join(kid[0].itertext())) if kid and kid[0].tag == "binary" else ("url", "".join(p.itertext()).strip())
        elif p.tag in ("token", "int"):
            d[n] = int(float(p.text))
        elif p.tag == "float":
            d[n] = float(p.text)
        else:
            d[n] = p.text
    return d


def _content_to_rgba(c, assets):
    kind, val = c
    if kind == "bin":
        raw = base64.b64decode(re.sub(r"\s+", "", val))
        return load_rgba(io.BytesIO(raw))
    if not val or val.lower() in ("none", "null"):
        return None
    f = find_asset(assets, val)
    if not f:
        pass
        return None
    return load_rgba(f)


def parse_color(tok):
    tok = tok.strip()
    if tok.startswith("#") and len(tok) == 7:
        return np.array([int(tok[i:i + 2], 16) for i in (1, 3, 5)], np.float32) / 255.0
    return brick_rgb(int(tok))


def build_from_rbxm(path, assets, tiles, overrides, face=None, torso_decal=True):
    root = ET.parse(path).getroot()
    sc = Scene()

    def walk(item):
        if item.get("class") == "Part":
            part(item)
        for c in item.findall("Item"):
            walk(c)

    def part(item):
        pr = _props(item)
        name = pr.get("Name", "")
        cf = pr["CFrame"]
        R = np.array([[cf["R00"], cf["R01"], cf["R02"]], [cf["R10"], cf["R11"], cf["R12"]],
                      [cf["R20"], cf["R21"], cf["R22"]]], np.float32)
        pos = np.array([cf["X"], cf["Y"], cf["Z"]], np.float32)
        size = pr.get("size") or pr.get("Size") or [2, 1, 1]
        if pr.get("Transparency", 0) > 0.99:
            return
        color = parse_color(overrides[name]) if name in overrides else brick_rgb(pr.get("BrickColor", 194))
        decals = {}
        mesh = None
        for c in item.findall("Item"):
            cp = _props(c)
            if c.get("class") == "Decal":
                tex = cp.get("Texture")
                if name == "Head" and cp.get("Name") == "face" and face:
                    tex = ("url", face)
                if cp.get("Name") == "roblox" and not torso_decal:
                    continue
                img = _content_to_rgba(tex, assets) if tex else None
                if img is not None:
                    decals[cp.get("Face", 5)] = img
            elif c.get("class") in ("SpecialMesh", "BlockMesh", "CylinderMesh"):
                mesh = cp
        if mesh and mesh.get("MeshType") == 0:                     
            decal = decals.get(5)
            m = sc.material(color=color, decal=decal)
            add_head(sc, R, pos, mesh.get("Scale", [1.25, 1.25, 1.25]), m)
            return
        if mesh and mesh.get("MeshType") == 5 and mesh.get("MeshId"):
            f = find_asset(assets, mesh["MeshId"][1])
            if f:
                tex = _content_to_rgba(mesh["TextureId"], assets) if mesh.get("TextureId") else None
                m = sc.material(color=color, decal=tex, wrap=True)
                add_filemesh(sc, R, pos, f, mesh.get("Scale", [1, 1, 1]), m)
                return
        mats = []
        for nid in range(6):
            st = pr.get(SURF_PROP[nid], 0)
            mats.append(sc.material(color=color, surf=(tiles.t[st], 1.0) if st in tiles.t else None, decal=decals.get(nid)))
        add_box(sc, R, pos, size, mats)

    for it in root.findall("Item"):
        walk(it)
    return sc.done()


                                                                              
                                                                           
                                                                              
def bilinear(tex, u, v, wrap):
    H, W = tex.shape[:2]
    x, y = u * W - 0.5, v * H - 0.5
    x0, y0 = np.floor(x), np.floor(y)
    fx, fy = (x - x0)[:, None], (y - y0)[:, None]
    x0, y0 = x0.astype(np.int64), y0.astype(np.int64)
    x1, y1 = x0 + 1, y0 + 1
    if wrap:
        x0, x1, y0, y1 = x0 % W, x1 % W, y0 % H, y1 % H
    else:
        x0, x1 = np.clip(x0, 0, W - 1), np.clip(x1, 0, W - 1)
        y0, y1 = np.clip(y0, 0, H - 1), np.clip(y1, 0, H - 1)
    return (tex[y0, x0] * (1 - fx) + tex[y0, x1] * fx) * (1 - fy) + (tex[y1, x0] * (1 - fx) + tex[y1, x1] * fx) * fy


class Camera:
    def __init__(self, scene, yaw, pitch, fov, aspect, margin=0.08, dist=None):
        P = scene.P.reshape(-1, 3)
        lo, hi = P.min(0), P.max(0)
        self.target = (lo + hi) / 2
        yw, pt = math.radians(yaw), math.radians(pitch)
        d = np.array([math.sin(yw) * math.cos(pt), math.sin(pt), math.cos(yw) * math.cos(pt)])
        self.f = -d / np.linalg.norm(d)
        self.r = np.cross(self.f, [0, 1, 0])
        self.r /= np.linalg.norm(self.r)
        self.u = np.cross(self.r, self.f)
        self.t = math.tan(math.radians(fov) / 2)
        self.aspect = aspect
        q = P - self.target
        pr, pu, pf = q @ self.r, q @ self.u, q @ self.f
        need = max(np.max(np.abs(pu) / (self.t * (1 - margin)) - pf), np.max(np.abs(pr) / (self.t * aspect * (1 - margin)) - pf))
        self.dist = dist if dist else float(need)
        self.eye = self.target - self.f * self.dist

    def project(self, W):
        q = W - self.eye
        x, y, z = q @ self.r, q @ self.u, q @ self.f
        return x, y, z


def sky_bg(cam, Wp, Hp, assets):
    names = {k: find_asset(assets, f"null_plainsky512_{k}.jpg") for k in ("ft", "bk", "lf", "rt", "up", "dn")}
    if not all(names.values()):
        pass
        g = np.linspace(0.45, 0.8, Hp)[:, None, None] * np.ones((1, Wp, 1))
        return np.concatenate([g * 0.6, g * 0.8, np.ones_like(g)], 2).astype(np.float32)
    tx = {k: np.asarray(Image.open(v).convert("RGB"), np.float32) / 255.0 for k, v in names.items()}
    ix = (np.arange(Wp) + 0.5) / Wp * 2 - 1
    iy = 1 - (np.arange(Hp) + 0.5) / Hp * 2
    dirs = (cam.f[None, None] + cam.r[None, None] * (ix[None, :, None] * cam.t * cam.aspect)
            + cam.u[None, None] * (iy[:, None, None] * cam.t))
    x, y, z = dirs[..., 0], dirs[..., 1], dirs[..., 2]
    ax, ay, az = np.abs(x), np.abs(y), np.abs(z)
    out = np.zeros((Hp, Wp, 3), np.float32)
    sel = [("rt", (ax >= ay) & (ax >= az) & (x > 0), z / ax.clip(1e-9), -y / ax.clip(1e-9)),
           ("lf", (ax >= ay) & (ax >= az) & (x <= 0), -z / ax.clip(1e-9), -y / ax.clip(1e-9)),
           ("up", (ay > ax) & (ay >= az) & (y > 0), -x / ay.clip(1e-9), z / ay.clip(1e-9)),
           ("dn", (ay > ax) & (ay >= az) & (y <= 0), x / ay.clip(1e-9), z / ay.clip(1e-9)),
           ("bk", (az > ax) & (az > ay) & (z > 0), -x / az.clip(1e-9), -y / az.clip(1e-9)),
           ("ft", (az > ax) & (az > ay) & (z <= 0), x / az.clip(1e-9), -y / az.clip(1e-9))]
    for k, m, u, v in sel:
        if m.any():
            out[m] = bilinear(tx[k], (u[m] + 1) / 2, (v[m] + 1) / 2, False)
    return out


def render(sc, cam, W, H, ss, bg, light, assets):
    Wp, Hp = W * ss, H * ss
    color = np.zeros((Hp, Wp, 3), np.float32)
    zinv = np.zeros((Hp, Wp), np.float32)
    cover = np.zeros((Hp, Wp), bool)
    x, y, z = cam.project(sc.P)                            
    z = np.maximum(z, 1e-4)
    sx = (x / (z * cam.t * cam.aspect) * 0.5 + 0.5) * Wp
    sy = (0.5 - y / (z * cam.t) * 0.5) * Hp
    iz = 1.0 / z
    L = np.asarray(light["dir"], np.float32)
    L /= np.linalg.norm(L)
    amb, dif = light["ambient"], light["diffuse"]
    for t in range(len(sc.P)):
        X, Y, IZ = sx[t], sy[t], iz[t]
        x0, x1 = max(int(math.floor(X.min())), 0), min(int(math.ceil(X.max())), Wp - 1)
        y0, y1 = max(int(math.floor(Y.min())), 0), min(int(math.ceil(Y.max())), Hp - 1)
        if x1 < x0 or y1 < y0:
            continue
        area = (X[1] - X[0]) * (Y[2] - Y[0]) - (X[2] - X[0]) * (Y[1] - Y[0])
        if abs(area) < 1e-9:
            continue
        gx, gy = np.meshgrid(np.arange(x0, x1 + 1, dtype=np.float32) + 0.5, np.arange(y0, y1 + 1, dtype=np.float32) + 0.5)
        w0 = ((X[2] - X[1]) * (gy - Y[1]) - (Y[2] - Y[1]) * (gx - X[1])) / area
        w1 = ((X[0] - X[2]) * (gy - Y[2]) - (Y[0] - Y[2]) * (gx - X[2])) / area
        w2 = 1.0 - w0 - w1
        s = w0 * IZ[0] + w1 * IZ[1] + w2 * IZ[2]
        eps = -1e-5
        m = (w0 >= eps) & (w1 >= eps) & (w2 >= eps) & (s > zinv[y0:y1 + 1, x0:x1 + 1])
        if not m.any():
            continue
        ys, xs = np.nonzero(m)
        q0, q1, q2 = w0[m] * IZ[0], w1[m] * IZ[1], w2[m] * IZ[2]
        sm = q0 + q1 + q2
        b = np.stack([q0 / sm, q1 / sm, q2 / sm], 1)                     
        att = np.einsum("nk,kj->nj", b, sc.A[t])                           
        nrm = np.einsum("nk,kj->nj", b, sc.N[t])
        nrm /= np.linalg.norm(nrm, axis=1, keepdims=True) + 1e-9
        mat = sc.mats[sc.M[t]]
        col = np.tile(mat["color"], (len(att), 1))
        if mat["surf"] is not None:
            tile, per = mat["surf"]
            col *= bilinear(tile, (att[:, 0] / per) % 1.0, (att[:, 1] / per) % 1.0, True)
        if mat["decal"] is not None:
            u, v = att[:, 2], att[:, 3]
            tex = bilinear(mat["decal"], u % 1.0 if mat["wrap"] else u, v % 1.0 if mat["wrap"] else v, mat["wrap"])
            valid = (att[:, 4] > 0) if not mat["wrap"] else np.ones(len(att), bool)
            if not mat["wrap"]:
                valid &= (u >= 0) & (u <= 1) & (v >= 0) & (v <= 1)
            a = (tex[:, 3] * valid)[:, None]
            col = col * (1 - a) + tex[:, :3] * valid[:, None]
        lit = amb + dif * np.clip(nrm @ L, 0, 1)
        col = np.clip(col * lit[:, None], 0, 1)
        yy, xx = ys + y0, xs + x0
        color[yy, xx] = col
        zinv[yy, xx] = sm
        cover[yy, xx] = True
    if bg is not None:
        bgp = bg if isinstance(bg, np.ndarray) else np.broadcast_to(np.asarray(bg, np.float32), (Hp, Wp, 3))
        color = np.where(cover[..., None], color, bgp)
        cover = np.ones_like(cover)
    c = (color * cover[..., None]).reshape(H, ss, W, ss, 3).sum((1, 3))
    a = cover.reshape(H, ss, W, ss).sum((1, 3)).astype(np.float32)
    rgb = c / np.maximum(a[..., None], 1)
    alpha = a / (ss * ss)
    out = np.concatenate([rgb, alpha[..., None]], 2)
    return Image.fromarray((np.clip(out, 0, 1) * 255 + 0.5).astype(np.uint8), "RGBA")


                                                                              
     
                                                                              
def default_asset(a, name):
    f = find_asset(a.assets, name)
    if not f:
        sys.exit(f"Required asset '{name}' was not found in {a.assets}/. Run: python rbxrender.py setup <file.msi>")
    return f


def common_render_args(p):
    p.add_argument("-o", "--out", default="render.png")
    p.add_argument("--assets", default="assets", help="Directory created by the setup command")
    p.add_argument("--size", default="512", help="Width or WIDTHxHEIGHT (default: 512)")
    p.add_argument("--ss", type=int, default=4, help="Supersampling factor (1 disables antialiasing)")
    p.add_argument("--yaw", type=float, default=30.0, help="Camera yaw angle in degrees")
    p.add_argument("--pitch", type=float, default=25.0, help="Camera pitch angle in degrees above the horizon")
    p.add_argument("--fov", type=float, default=70.0, help="Vertical field of view (default: 70)")
    p.add_argument("--margin", type=float, default=0.08, help="Padding around the object (0-0.5)")
    p.add_argument("--dist", type=float, default=None, help="Fixed camera distance (default: fit the object)")
    p.add_argument("--bg", default="transparent", help="Background: transparent, sky, or #RRGGBB")
    p.add_argument("--light-dir", default="0.35,0.75,0.55", help="Light direction in world coordinates (x,y,z)")
    p.add_argument("--ambient", type=float, default=0.50)
    p.add_argument("--diffuse", type=float, default=0.70)
    p.add_argument("--stud-variant", type=int, default=0, help="Stud tile variant from Surfaces.png (0-7)")


def parse_size(s):
    w, _, h = s.lower().partition("x")
    return int(w), int(h or w)


def do_render(a, sc):
    W, H = parse_size(a.size)
    cam = Camera(sc, a.yaw, a.pitch, a.fov, W / H, a.margin, a.dist)
    light = dict(dir=[float(v) for v in a.light_dir.split(",")], ambient=a.ambient, diffuse=a.diffuse)
    if a.bg == "transparent":
        bg = None
    elif a.bg == "sky":
        bg = sky_bg(cam, W * a.ss, H * a.ss, a.assets)
    else:
        bg = parse_color(a.bg)
    img = render(sc, cam, W, H, a.ss, bg, light, a.assets)
    img.save(a.out)
    print(f"Saved: {a.out} ({W}x{H}, {len(sc.P)} triangles)")


def cmd_render(a):
    model = a.model or default_asset(a, "character.rbxm")
    tiles = Tiles(default_asset(a, "Surfaces.png"), a.stud_variant)
    over = {}
    for c in a.color or []:
        k, _, v = c.partition("=")
        over[k.strip()] = v
    face = a.face
    sc = build_from_rbxm(model, a.assets, tiles, over, face=face, torso_decal=not a.no_torso_decal)
    do_render(a, sc)


def cmd_mesh(a):
    sc = Scene()
    tex = load_rgba(a.texture if os.path.isfile(a.texture or "") else default_asset(a, a.texture)) if a.texture else None
    m = sc.material(color=parse_color(a.color), decal=tex, wrap=True)
    add_filemesh(sc, np.eye(3, dtype=np.float32), np.zeros(3, np.float32), a.mesh, (1, 1, 1), m,
                 mesh_scale=a.mesh_scale, flip_v=not a.no_flip_v)
    do_render(a, sc.done())


def cmd_colors(a):
    for k in sorted(BRICK):
        n, r, g, b = BRICK[k]
        print(f"{k:4d}  #{r:02x}{g:02x}{b:02x}  {n}")


def main():
    ap = argparse.ArgumentParser(description="Roblox character and mesh renderer", formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = ap.add_subparsers(dest="cmd", required=True)
    s = sp.add_parser("setup", help="Extract assets from an MSI file")
    s.add_argument("msi")
    s.add_argument("--assets", default="assets")
    s.add_argument("--all", action="store_true", help="Extract all files, including DLLs and debug symbols")
    s.set_defaults(fn=cmd_setup)
    r = sp.add_parser("render", help="Render an RBXM model (default: character.rbxm)")
    r.add_argument("model", nargs="?")
    common_render_args(r)
    r.add_argument("-c", "--color", action="append", help='PartName=BrickColor|#RRGGBB (e.g. Torso=21 / "Left Arm=#ffcc99")')
    r.add_argument("--face", help="Face PNG file (replaces face.png)")
    r.add_argument("--no-torso-decal", action="store_true")
    r.set_defaults(fn=cmd_render)
    m = sp.add_parser("mesh", help="Render a standalone .mesh file (gear or extras)")
    m.add_argument("mesh")
    common_render_args(m)
    m.add_argument("-t", "--texture")
    m.add_argument("--color", default="194", help="BrickColor or #RRGGBB (used when no texture is available)")
    m.add_argument("--mesh-scale", type=float, default=0.5, help="Scale factor for v1.00 mesh coordinates")
    m.add_argument("--no-flip-v", action="store_true")
    m.set_defaults(fn=cmd_mesh)
    c = sp.add_parser("colors", help="List the BrickColor palette")
    c.set_defaults(fn=cmd_colors)
    a = ap.parse_args()
    a.fn(a)


if __name__ == "__main__":
    main()
