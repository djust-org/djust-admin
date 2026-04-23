# Migrating from `djust-admin` to `djust.admin_ext`

This repo is deprecated. All functionality is now in the `djust` core package, under `djust.admin_ext` (renamed from `admin` to avoid clashing with `django.contrib.admin`).

## 1. Replace the install

```diff
- pip install djust-admin
+ pip install djust
```

## 2. Update imports

Grep-replace the top-level package name:

```bash
# macOS:
grep -rl 'djust_admin' . | xargs sed -i '' 's/djust_admin/djust.admin_ext/g'
# Linux:
grep -rl 'djust_admin' . | xargs sed -i     's/djust_admin/djust.admin_ext/g'
```

## 3. Import mapping

| Before                                    | After                                 |
| ----------------------------------------- | ------------------------------------- |
| `from djust_admin import X`               | `from djust.admin_ext import X`       |
| `import djust_admin`                      | `from djust import admin_ext`         |
| `'djust_admin'` in `INSTALLED_APPS`       | `'djust.admin_ext'`                   |
| `djust_admin.autodiscover()`              | `djust.admin_ext.autodiscover()`      |

All public names (`DjustAdminSite`, `DjustModelAdmin`, `AdminPlugin`, `AdminPage`, `AdminWidget`, `NavItem`, `register`, `action`, `display`, `site`, `autodiscover`) are re-exported from `djust.admin_ext` with the same signatures.

## 4. Remove the old dep

Once imports are migrated and tests pass, remove `djust-admin` from your `pyproject.toml` / `requirements.txt`. The shim package depends on `djust>=0.5.6rc1` so djust is already installed.
