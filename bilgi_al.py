from PyQt5.QtCore import QVariant
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from qgis.core import *
import qgis.utils

#katmanlar=list()

class diyalog(QDialog):
    def __init__(self,iface,ebeveyn=None):
        super(diyalog,self).__init__(ebeveyn)
        self.iface=iface
        katmanlar=list()
        for lyr in self.iface.mapCanvas().layers():
            if lyr.geometryType() == QgsWkbTypes.LineGeometry:
                katmanlar.append(lyr.name())
        etk1=QLabel("Kaynak Katman")
        etk2=QLabel("Kolon")
        etk3=QLabel("Hedef Katman")
        etk4=QLabel("Kolon")
        etk6=QLabel("Tampon Uz.")
        self.bufdist=QLineEdit("100")
        self.pbar=QProgressBar(self)
        but=QPushButton("Uygula")
        but.clicked.connect(self.uygula)
        but.setToolTip("İşlem geri alınamaz!")
        self.kombt1=QComboBox()
        self.kombt1.addItems(katmanlar) #Katman listesini kombobox a alıyoruz.
        self.kombt2=QComboBox()
        self.kombt2.addItems(katmanlar) 
        self.kombt1f=QComboBox()
        self.kombt2f=QComboBox()
        self.kombt1.currentTextChanged.connect(self.komboyap)
        self.kombt2.currentTextChanged.connect(self.komboyap)
        kut=QGridLayout()
        kut.addWidget(etk1,0,1)
        kut.addWidget(etk2,1,1)
        kut.addWidget(etk3,2,1)
        kut.addWidget(etk4,3,1)
        kut.addWidget(but,5,2)
        kut.addWidget(self.kombt1,0,2)
        kut.addWidget(self.kombt2,2,2) 
        kut.addWidget(self.pbar,5,1)
        kut.addWidget(self.kombt1f,1,2)
        kut.addWidget(self.kombt2f,3,2)
        kut.addWidget(etk6,4,1)
        kut.addWidget(self.bufdist,4,2)
        self.setLayout(kut)
        self.setWindowTitle("Çizgiden Bilgi Al") 
        self.setGeometry(50,50,300,250) 
        self.lyra=None
        self.lyrp=None
    def uygula(self):
        if self.kombt1.currentText()!=self.kombt2.currentText():
            if self.lyra and self.lyrp:
                f1=self.lyra.fields().indexOf(self.kombt1f.currentText())
                f2=self.lyrp.fields().indexOf(self.kombt2f.currentText())
                self.duzenle(f1,f2)
    def komboyap(self,val):
# Çizgi katmanlarının kolonları doldurulur. kat1 kaynak, kat2 hedef
        self.kombt1f.clear()
        self.kombt2f.clear()
        kat1=self.kombt1.currentText()
        kat2=self.kombt2.currentText()
        for lyr in self.iface.mapCanvas().layers():
            if kat1==lyr.name():
                self.lyra=lyr
                for f in lyr.fields():
                  self.kombt1f.addItem(f.name())
            if kat2==lyr.name():
                self.lyrp=lyr
                for f in lyr.fields():
                  self.kombt2f.addItem(f.name())

    def duzenle(self,f1,f2):
        dbuf=float(self.bufdist.text())
#Kaynak ve hedef katman editable ise kapatıyoruz.
        if self.lyra.isEditable():
            self.lyra.commitChanges()
        if self.lyrp.isEditable():
            self.lyrp.commitChanges()
#Hedef katmanı edtable yapıyoruz. 
        self.lyrp.startEditing()
#Kaynak katmanda çizgiyi alıp buffer geçiriyoruz. Hedef feature'ların buffer içindekileri bulup symbol katmanlarını aktarıyoruz. 
        i=0
        j=0
        k=0
        ii=self.lyra.featureCount()
        for feat_a in self.lyra.getFeatures():
            geom_a=feat_a.geometry()
            geom_buf=geom_a.buffer(dbuf,5)
            j+=1
            yzd=int(100*j/ii)
            if yzd%10==0 and yzd>0:
                #print(">>>",yzd)
                self.pbar.setValue(yzd)
            feats_p=self.lyrp.getFeatures()
            for feat_p in feats_p:
                k+=1
                geom_p=feat_p.geometry()
                if geom_p.within(geom_buf):
                    feat_p[f2]=feat_a[f1]
                    self.lyrp.updateFeature(feat_p)
                    i+=1
        self.lyrp.commitChanges()
        print(f"{i} işlem!")      

##Açık katmanların listesini yap
#for lyr in iface.mapCanvas().layers():
#    katmanlar.append(lyr.name())
    
#penc=diyalog()
#penc.show()

