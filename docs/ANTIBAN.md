# Setup

## 1. If you use Bash, make sure execute permission

```sh
chmod +x bin/*
```

## 2. Init antiban

```sh
bin/antiban.sh init
# Or
python3 -m scripts.antiban init
```

---

### Manually

Check whether APIs are safe

```sh
bin/antiban.sh check
# Or
python3 -m scripts.antiban check
```

Mark all APIS safe

```sh
bin/antiban.sh safe
# Or
python3 -m scripts.antiban safe
```
