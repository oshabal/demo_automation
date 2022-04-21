import pytest
#from playwright.sync_api import expect

def test_pages(path):
    path.home()
    path.showcase()
    path.packshot_generator()
    path.careers()

@pytest.mark.parametrize("model", ["leather-chair", "Colorful_Wine", "pet-rock"])
def test_upload_3D_model(path, packshot_generator, model):
    path.packshot_generator()
    packshot_generator.upload_3D_model(model)

@pytest.mark.parametrize("model", [0, 1, 2])
def test_upload_sample_3D_model(path, packshot_generator, model):
    path.packshot_generator()
    packshot_generator.upload_sample_3D_model(model)

def test_colorpicker(path, packshot_generator):
    path.packshot_generator()
    packshot_generator.upload_sample_3D_model()
    packshot_generator.background.hsv()
    packshot_generator.background.hex()
    packshot_generator.background.rgb("66, 245, 206")
    packshot_generator.background.hsl()

@pytest.mark.parametrize(
    "model, shadow, transparent, four_k, background", [
    pytest.param(None, True, True, False, None),
    pytest.param("Colorful_Wine", True, True, False, "#4287f5")
    ])
def test_case(path, packshot_generator, model, shadow, transparent, four_k, background):
    path.packshot_generator()
    packshot_generator.upload_sample_3D_model(model)
    packshot_generator.shadows(shadow)
    packshot_generator.transparent(transparent)
    packshot_generator.four_k_resolution(four_k)
    packshot_generator.background.hex(background)
    packshot_generator.drag()
    packshot_generator.zoom_in()
    packshot_generator.zoom_out()
    packshot_generator.add_image()
    packshot_generator.select_image()
    packshot_generator.delete_image()
    packshot_generator.generate_images()
    packshot_generator.download_all()
